import logging

from sqlalchemy.orm import Session

from backend.app.integrations.jobs.base import JobProvider
from backend.app.integrations.jobs.greenhouse import GreenhouseProvider
from backend.app.models.job_description import JobDescription
from backend.app.repositories.job_repository import JobRepository
from backend.app.repositories.parsed_job_repository import ParsedJobRepository
from backend.app.services.ai.job_filter_service import JobFilterService
from backend.app.services.parsed_job_service import ParsedJobService

logger = logging.getLogger(__name__)


class JobDiscoveryService:
    """
    Discovers jobs from providers,
    filters irrelevant jobs,
    saves relevant jobs,
    and automatically parses them.
    """

    def __init__(self, db: Session):

        self.job_repository = JobRepository(db)

        parsed_job_repository = ParsedJobRepository(db)

        self.parsed_job_service = ParsedJobService(
            repository=parsed_job_repository
        )

        self.providers: list[JobProvider] = [
    GreenhouseProvider(),
]

    async def discover_and_save_jobs(
        self,
        user_id: int,
        keywords: list[str],
        location: str | None = None,
        remote_only: bool = False,
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

                print("\n" + "=" * 70)
                print(f"Provider: {provider.provider_name}")
                print(f"Jobs Returned: {len(jobs)}")
                print("=" * 70)

                logger.info(
                    "Provider '%s' returned %d jobs.",
                    provider.provider_name,
                    len(jobs),
                )

                for job_data in jobs:

                    title = job_data.get("title", "")
                    description = job_data.get("description", "")

                    filter_result = JobFilterService.filter_job(
                        title=title,
                        description=description,
                    )

                    print(f"\nTitle      : {title}")
                    print(f"Accepted   : {filter_result.accepted}")
                    print(f"Score      : {filter_result.score}")
                    print(f"Confidence : {filter_result.confidence}")
                    print(f"Reason     : {filter_result.reason}")
                    print("-" * 70)

                    logger.info(
                        "Job='%s' | Score=%d | %s",
                        title,
                        filter_result.score,
                        filter_result.reason,
                    )

                    if not filter_result.accepted:

                        skipped_count += 1

                        print(f"❌ Rejected: {title}")

                        logger.info(
                            "Rejected: %s",
                            title,
                        )

                        continue

                    print(f"✅ Accepted: {title}")

                    logger.info(
                        "Accepted: %s",
                        title,
                    )

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

                    print(f"💾 Saved: {title}")

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

                print(f"❌ Provider failed: {provider.provider_name}")

        print("\n" + "=" * 70)
        print("JOB DISCOVERY SUMMARY")
        print(f"Saved Jobs   : {saved_count}")
        print(f"Skipped Jobs : {skipped_count}")
        print("=" * 70 + "\n")

        logger.info("==================================================")
        logger.info("Job Discovery Complete")
        logger.info("Saved Jobs   : %d", saved_count)
        logger.info("Skipped Jobs : %d", skipped_count)
        logger.info("==================================================")

        return saved_jobs