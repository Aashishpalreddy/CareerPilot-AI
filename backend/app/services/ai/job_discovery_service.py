import logging

from sqlalchemy.orm import Session

from backend.app.integrations.jobs.base import JobProvider
from backend.app.integrations.jobs.greenhouse import GreenhouseProvider
from backend.app.integrations.jobs.remoteok import RemoteOKProvider
from backend.app.models.job_description import JobDescription
from backend.app.repositories.job_repository import JobRepository
from backend.app.repositories.parsed_job_repository import ParsedJobRepository
from backend.app.services.ai.job_filter_service import JobFilterService
from backend.app.services.parsed_job_service import ParsedJobService

logger = logging.getLogger(__name__)


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
            RemoteOKProvider(),
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

        saved_jobs: list[JobDescription] = []
        saved_count = 0
        skipped_count = 0

        for provider in self.providers:
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

                for job_data in jobs:
                    title = job_data.get("title", "")
                    description = job_data.get("description", "")

                    # Apply additional filters if provided
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

                    filter_result = JobFilterService.filter_job(
                        title=title,
                        description=description,
                    )

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

                    logger.info("Accepted: %s", title)

                    job = JobDescription(
                        user_id=user_id,
                        title=title,
                        company=job_data.get("company"),
                        location=job_data.get("location"),
                        source=job_data.get("source"),
                        job_url=job_data.get("job_url"),
                        raw_text=description,
                    )

                    saved_job = self.job_repository.create(job)
                    self.parsed_job_service.parse_job(saved_job)
                    saved_jobs.append(saved_job)
                    saved_count += 1

                    logger.info(
                        "Saved '%s' (Score=%d, Confidence=%.2f)",
                        title,
                        filter_result.score,
                        filter_result.confidence,
                    )

            except Exception:
                logger.exception(
                    "Failed provider: %s",
                    provider.provider_name,
                )

        logger.info(
            "Job Discovery Complete — Saved: %d, Skipped: %d",
            saved_count,
            skipped_count,
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