import asyncio
import logging

from sqlalchemy.orm import Session

from backend.app.integrations.jobs.adzuna import AdzunaProvider
from backend.app.integrations.jobs.base import JobProvider
from backend.app.integrations.jobs.greenhouse import GreenhouseProvider
from backend.app.integrations.jobs.lever import LeverProvider
from backend.app.integrations.jobs.remoteok import RemoteOKProvider
from backend.app.integrations.jobs.remotive import RemotiveProvider
from backend.app.models.job_description import JobDescription
from backend.app.repositories.job_repository import JobRepository
from backend.app.repositories.parsed_job_repository import ParsedJobRepository
from backend.app.services.ai.job_filter_service import JobFilterService
from backend.app.services.parsed_job_service import ParsedJobService

logger = logging.getLogger(__name__)

# How many AI relevance-filter calls to run concurrently. Keeps discovery
# from making Claude calls one-at-a-time (which is what made a single
# search take minutes) while not slamming the API with hundreds at once.
MAX_CONCURRENT_FILTER_CALLS = 8


class JobDiscoveryService:
    """
    Discovers jobs from providers, filters irrelevant jobs,
    saves relevant jobs, and automatically parses them.
    """

    def __init__(self, db: Session):
        self.job_repository = JobRepository(db)
        parsed_job_repository = ParsedJobRepository(db)
        self.parsed_job_service = ParsedJobService(
            repository=parsed_job_repository
        )
        self.providers: list[JobProvider] = [
            GreenhouseProvider(),
            LeverProvider(),
            RemoteOKProvider(),
            RemotiveProvider(),
            AdzunaProvider(),
        ]

    async def discover_and_save_jobs(
        self,
        user_id: int,
        keywords: list[str],
        location: str | None = None,
        remote_only: bool = False,
        job_type: str | None = None,
        experience_level: str | None = None,
        max_results_per_provider: int = 50,
    ) -> list[JobDescription]:

        # Each search replaces the tracked-jobs list rather than piling on
        # top of the last one. Manually-added jobs and anything already
        # tailored/applied to are preserved (see delete_discovered_for_user).
        removed_count = self.job_repository.delete_discovered_for_user(user_id)
        if removed_count:
            logger.info(
                "Cleared %d previously discovered job(s) for user %s ahead of new search.",
                removed_count,
                user_id,
            )

        saved_jobs: list[JobDescription] = []
        saved_count = 0
        skipped_count = 0
        duplicate_count = 0

        semaphore = asyncio.Semaphore(MAX_CONCURRENT_FILTER_CALLS)

        async def run_filter(job_data: dict):
            title = job_data.get("title", "")
            description = job_data.get("description", "")
            async with semaphore:
                filter_result = await asyncio.to_thread(
                    JobFilterService.filter_job,
                    title=title,
                    description=description,
                )
            return job_data, filter_result

        async def fetch_provider(provider: JobProvider) -> list[dict]:
            try:
                jobs = await provider.search_jobs(
                    keywords=keywords,
                    location=location,
                    remote_only=remote_only,
                    max_results=max_results_per_provider,
                )
                logger.info(
                    "Provider '%s' returned %d jobs.",
                    provider.provider_name,
                    len(jobs),
                )
                return jobs
            except Exception:
                logger.exception("Failed provider: %s", provider.provider_name)
                return []

        # Query every provider concurrently instead of one at a time — with
        # four sources, waiting on each in turn adds up fast.
        provider_results = await asyncio.gather(
            *(fetch_provider(provider) for provider in self.providers)
        )

        # Cheap keyword filters run up front, across all providers, so the
        # (comparatively expensive) AI relevance check only runs on real
        # candidates.
        candidates = []
        for jobs in provider_results:
            for job_data in jobs:
                title = job_data.get("title", "")
                description = job_data.get("description", "")

                if job_type and not self._matches_job_type(
                    title, description, job_type
                ):
                    skipped_count += 1
                    continue

                if experience_level and not self._matches_experience(
                    title, description, experience_level
                ):
                    skipped_count += 1
                    continue

                candidates.append(job_data)

        # AI relevance filtering runs concurrently (bounded by
        # MAX_CONCURRENT_FILTER_CALLS) instead of one Claude call at a
        # time — this is what previously made discovery take minutes.
        filter_outcomes = await asyncio.gather(
            *(run_filter(job_data) for job_data in candidates)
        )

        for job_data, filter_result in filter_outcomes:
            title = job_data.get("title", "")
            description = job_data.get("description", "")

            logger.debug(
                "Job='%s' | Score=%d | Confidence=%.2f | %s",
                title,
                filter_result.score,
                filter_result.confidence,
                filter_result.reason,
            )

            if not filter_result.accepted:
                skipped_count += 1
                logger.debug("Rejected: %s", title)
                continue

            job_url = job_data.get("job_url")
            if self.job_repository.get_by_user_and_url(user_id, job_url):
                duplicate_count += 1
                logger.debug("Duplicate (already tracked): %s", title)
                continue

            logger.info("Accepted: %s", title)

            job = JobDescription(
                user_id=user_id,
                title=title,
                company=job_data.get("company"),
                location=job_data.get("location"),
                source=job_data.get("source"),
                job_url=job_url,
                raw_text=description,
            )

            saved_job = self.job_repository.create(job)
            # Fast, rule-based parse only — no per-job Claude call, so a
            # search returns in seconds instead of blocking on one API
            # call per job. Full AI parsing happens on demand when the
            # user opens an individual job.
            self.parsed_job_service.parse_job(saved_job, use_ai=False)
            saved_jobs.append(saved_job)
            saved_count += 1

            logger.info(
                "Saved '%s' (Score=%d, Confidence=%.2f)",
                title,
                filter_result.score,
                filter_result.confidence,
            )

        logger.info(
            "Job Discovery Complete — Saved: %d, Skipped: %d, Duplicates: %d",
            saved_count,
            skipped_count,
            duplicate_count,
        )

        return saved_jobs

    @staticmethod
    def _matches_job_type(
        title: str,
        description: str,
        job_type: str,
    ) -> bool:
        """Simple keyword check for job type filtering."""
        text = f"{title} {description}".lower()
        job_type = job_type.lower().strip()

        if job_type == "full-time":
            # Accept if explicitly full-time OR no contract/part-time markers
            if "contract" in text or "part-time" in text or "part time" in text:
                return False
            return True
        elif job_type == "contract":
            return "contract" in text or "freelance" in text or "consulting" in text
        elif job_type == "part-time":
            return "part-time" in text or "part time" in text
        return True

    @staticmethod
    def _matches_experience(
        title: str,
        description: str,
        experience_level: str,
    ) -> bool:
        """Simple keyword check for experience level filtering."""
        text = f"{title} {description}".lower()
        level = experience_level.lower().strip()

        if level == "entry":
            return any(
                kw in text
                for kw in [
                    "entry", "junior", "jr", "associate", "intern",
                    "new grad", "graduate", "0-2 years", "1-2 years",
                    "0-1 years", "early career",
                ]
            )
        elif level == "mid":
            return any(
                kw in text
                for kw in [
                    "mid", "intermediate", "2-5 years", "3-5 years",
                    "2+ years", "3+ years",
                ]
            ) or not any(
                kw in text
                for kw in [
                    "senior", "sr.", "lead", "principal", "staff",
                    "director", "vp", "junior", "jr.", "intern",
                ]
            )
        elif level == "senior":
            return any(
                kw in text
                for kw in [
                    "senior", "sr.", "lead", "principal", "staff",
                    "architect", "5+ years", "7+ years", "10+ years",
                ]
            )
        return True