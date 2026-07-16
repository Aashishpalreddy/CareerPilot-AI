import logging

from sqlalchemy.orm import Session

from backend.app.models.saved_job import SavedJob
from backend.app.models.user import User
from backend.app.repositories.parsed_job_repository import ParsedJobRepository
from backend.app.repositories.parsed_resume_repository import ParsedResumeRepository
from backend.app.repositories.resume_repository import ResumeRepository
from backend.app.repositories.saved_job_repository import SavedJobRepository
from backend.app.services.ai.apply_classifier_service import ApplyClassifierService
from backend.app.services.ai.cover_letter_service import CoverLetterService
from backend.app.services.ai.job_discovery_service import JobDiscoveryService
from backend.app.services.ai.recruiter_contact_service import RecruiterContactService
from backend.app.services.ai.auto_apply_service import AutoApplyService
from backend.app.services.match_service import MatchService
from backend.app.services.resume_tailor_service import ResumeTailorService
import asyncio

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
        job_type: str | None = None,
        experience_level: str | None = None,
    ) -> list[SavedJob]:

        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.warning("User %s not found; skipping pipeline.", user_id)
            return []

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
            job_type=job_type,
            experience_level=experience_level,
        )

        saved: list[SavedJob] = []

        for job in discovered_jobs:

            if self.saved_job_repository.get_by_user_and_job(user_id, job.id):
                continue

            match = await asyncio.to_thread(
                self.match_service.match_resume_to_job,
                resume_id=resume.id,
                job_id=job.id,
            )

            if match is None or match.match_score < MIN_MATCH_SCORE_FOR_TAILORING:
                continue

            tailor_result = await asyncio.to_thread(
                self.resume_tailor_service.tailor_resume,
                resume_id=resume.id,
                job_id=job.id,
            )

            cover_letter_result = await asyncio.to_thread(
                self.cover_letter_service.generate_cover_letter,
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
                    tailor_result.tailored_summary if tailor_result else None
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

            created_saved_job = self.saved_job_repository.create(saved_job)
            saved.append(created_saved_job)
            
            # If eligible, run Auto Apply
            if classification.auto_apply_eligible:
                name_parts = user.full_name.split(" ", 1)
                first_name = name_parts[0]
                last_name = name_parts[1] if len(name_parts) > 1 else ""

                user_info = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": user.email,
                    "phone": getattr(user, "phone", "1234567890")
                }
                
                # We would normally write out the tailored resume to a temporary PDF file here
                # and pass its path to `resume_path`.
                success = await AutoApplyService.apply_to_job(
                    job_url=classification.apply_url or job.job_url,
                    user_info=user_info,
                    resume_path=resume.file_path,
                    cover_letter_text=cover_letter_result.cover_letter_text if cover_letter_result else None,
                )
                
                if success:
                    created_saved_job.status = "applied"
                    self.saved_job_repository.update(created_saved_job)

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
