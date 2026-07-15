import logging

from sqlalchemy.orm import Session

from backend.app.models.saved_job import SavedJob
from backend.app.repositories.parsed_job_repository import ParsedJobRepository
from backend.app.repositories.parsed_resume_repository import ParsedResumeRepository
from backend.app.repositories.resume_repository import ResumeRepository
from backend.app.repositories.saved_job_repository import SavedJobRepository
from backend.app.services.ai.apply_classifier_service import ApplyClassifierService
from backend.app.services.ai.cover_letter_service import CoverLetterService
from backend.app.services.ai.job_discovery_service import JobDiscoveryService
from backend.app.services.ai.recruiter_contact_service import RecruiterContactService
from backend.app.services.match_service import MatchService
from backend.app.services.resume_tailor_service import ResumeTailorService

logger = logging.getLogger(__name__)

# Only pre-generate tailored materials for jobs that clear this bar, to
# avoid burning LLM calls (and the person's time) on weak matches.
MIN_MATCH_SCORE_FOR_TAILORING = 40.0


class DailyPipelineService:
    """
    The end-to-end automation described in the product goal:
    every run, look for new jobs, keep the ones that fit the resume,
    and have tailored resume + cover letter + apply links ready to go
    before the person ever opens the app.
    """

    def __init__(self, db: Session):
        self.db = db

        self.resume_repository = ResumeRepository(db)
        self.parsed_resume_repository = ParsedResumeRepository(db)
        self.parsed_job_repository = ParsedJobRepository(db)
        self.saved_job_repository = SavedJobRepository(db)

        self.job_discovery_service = JobDiscoveryService(db)

        self.match_service = MatchService(
            parsed_resume_repository=self.parsed_resume_repository,
            parsed_job_repository=self.parsed_job_repository,
        )

        self.resume_tailor_service = ResumeTailorService(
            parsed_resume_repository=self.parsed_resume_repository,
            parsed_job_repository=self.parsed_job_repository,
        )

        self.cover_letter_service = CoverLetterService(
            parsed_resume_repository=self.parsed_resume_repository,
            parsed_job_repository=self.parsed_job_repository,
        )

    async def run_for_user(
        self,
        user_id: int,
        keywords: list[str],
        location: str | None = None,
        remote_only: bool = False,
    ) -> list[SavedJob]:

        resume = self.resume_repository.get_default(user_id)

        if resume is None:
            logger.warning(
                "User %s has no default resume set; skipping pipeline.",
                user_id,
            )
            return []

        discovered_jobs = await self.job_discovery_service.discover_and_save_jobs(
            user_id=user_id,
            keywords=keywords,
            location=location,
            remote_only=remote_only,
        )

        saved: list[SavedJob] = []

        for job in discovered_jobs:

            if self.saved_job_repository.get_by_user_and_job(user_id, job.id):
                continue

            match = self.match_service.match_resume_to_job(
                resume_id=resume.id,
                job_id=job.id,
            )

            if match is None or match.match_score < MIN_MATCH_SCORE_FOR_TAILORING:
                continue

            tailor_result = self.resume_tailor_service.tailor_resume(
                resume_id=resume.id,
                job_id=job.id,
            )

            cover_letter_result = self.cover_letter_service.generate_cover_letter(
                resume_id=resume.id,
                job_id=job.id,
            )

            classification = ApplyClassifierService.classify(job.job_url)

            recruiter_links = RecruiterContactService.build_contact_links(
                company=job.company or "",
            )

            saved_job = SavedJob(
                user_id=user_id,
                job_id=job.id,
                resume_id=resume.id,
                match_score=match.match_score,
                tailored_resume_text=(
                    tailor_result.tailored_resume_text if tailor_result else None
                ),
                cover_letter_text=(
                    cover_letter_result.cover_letter_text
                    if cover_letter_result
                    else None
                ),
                apply_url=classification.apply_url,
                auto_apply_eligible=classification.auto_apply_eligible,
                recruiter_links=recruiter_links,
                status="saved",
            )

            saved.append(self.saved_job_repository.create(saved_job))

            logger.info(
                "Saved job %s (%s) for user %s, match_score=%.1f, "
                "auto_apply_eligible=%s",
                job.title,
                job.company,
                user_id,
                match.match_score,
                classification.auto_apply_eligible,
            )

        return saved
