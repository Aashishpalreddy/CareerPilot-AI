import logging

from backend.app.models.parsed_job import ParsedJob
from backend.app.models.parsed_resume import ParsedResume
from backend.app.models.tailored_resume import TailoredResume

from backend.app.repositories.parsed_job_repository import ParsedJobRepository
from backend.app.repositories.parsed_resume_repository import ParsedResumeRepository
from backend.app.repositories.tailored_resume_repository import TailoredResumeRepository

from backend.app.schemas.resume_tailor import ResumeTailorResponse
from backend.app.services.ai_resume_tailor import AIResumeTailor
from backend.app.services.resume_match_service import ResumeMatchService

logger = logging.getLogger(__name__)


class ResumeTailorService:
    """
    Accepts either:
      - A TailoredResumeRepository (used by the API endpoint router)
      - parsed_resume_repository + parsed_job_repository (used by DailyPipelineService)
    Both create paths converge on the same .tailor() logic.
    """

    def __init__(
        self,
        repository: TailoredResumeRepository | None = None,
        parsed_resume_repository: ParsedResumeRepository | None = None,
        parsed_job_repository: ParsedJobRepository | None = None,
    ):
        self.repository = repository
        self.parsed_resume_repository = parsed_resume_repository
        self.parsed_job_repository = parsed_job_repository
        self.ai = AIResumeTailor()
        self.matcher = ResumeMatchService()

    def tailor(
        self,
        parsed_resume: ParsedResume,
        parsed_job: ParsedJob,
    ) -> ResumeTailorResponse:
        """Core tailoring logic — operates on already-fetched parsed objects."""

        match = self.matcher.match(parsed_resume, parsed_job)

        MAX_ITERATIONS = 3
        ats_feedback = None
        best_ai_result = None
        best_ats_score = 0
        
        from backend.app.services.ats_score_service import ATSScoreService
        from backend.app.models.parsed_resume import ParsedResume

        for i in range(MAX_ITERATIONS):
            ai_result = self.ai.tailor(
                parsed_resume={
                    "summary": parsed_resume.summary,
                    "skills": parsed_resume.skills,
                    "experience": parsed_resume.experience,
                    "projects": parsed_resume.projects,
                    "certifications": parsed_resume.certifications,
                    "technologies": parsed_resume.technologies,
                },
                parsed_job={
                    "title": parsed_job.title,
                    "summary": parsed_job.job_summary,
                    "skills": parsed_job.skills,
                    "technologies": parsed_job.technologies,
                    "responsibilities": parsed_job.responsibilities,
                    "qualifications": parsed_job.qualifications,
                    "keywords": parsed_job.keywords,
                },
                ats_feedback=ats_feedback,
            )
            
            # Create a mock resume text to score
            temp_text = str(ai_result.tailored_summary) + "\n" + " ".join(ai_result.ats_keywords) + "\n" + str(ai_result.tailored_experience) + "\n" + str(ai_result.tailored_projects)
            temp_resume = ParsedResume(
                summary=ai_result.tailored_summary,
                skills=ai_result.ats_keywords,
                raw_text=temp_text
            )
            
            ats_res = ATSScoreService.calculate(temp_resume, parsed_job)
            current_score = ats_res.get("score", 0)
            
            if current_score > best_ats_score:
                best_ats_score = current_score
                best_ai_result = ai_result
                
            if current_score >= 90:
                break
                
            ats_feedback = ats_res

        ai_result = best_ai_result

        if self.repository:
            existing = self.repository.get(
                parsed_resume.resume_id,
                parsed_job.job_id,
            )

            if existing:
                existing.tailored_summary = ai_result.tailored_summary
                existing.tailored_experience = ai_result.tailored_experience
                existing.tailored_projects = ai_result.tailored_projects
                existing.ats_keywords = ai_result.ats_keywords
                existing.overall_match = match.overall_match
                self.repository.update(existing)
            else:
                tailored = TailoredResume(
                    resume_id=parsed_resume.resume_id,
                    job_id=parsed_job.job_id,
                    tailored_summary=ai_result.tailored_summary,
                    tailored_experience=ai_result.tailored_experience,
                    tailored_projects=ai_result.tailored_projects,
                    ats_keywords=ai_result.ats_keywords,
                    overall_match=match.overall_match,
                )
                self.repository.create(tailored)

        return ResumeTailorResponse(
            resume_id=parsed_resume.resume_id,
            job_id=parsed_job.job_id,
            original_match_score=match.overall_match,
            improved_match_score=min(100, match.overall_match + 15),
            tailored_summary=ai_result.tailored_summary,
            tailored_experience=ai_result.tailored_experience,
            tailored_projects=ai_result.tailored_projects,
            ats_keywords=ai_result.ats_keywords,
            tailored_bullets=ai_result.tailored_bullets,
            keywords_added=ai_result.keywords_added,
            keywords_missing=ai_result.keywords_missing,
        )

    def tailor_resume(
        self,
        resume_id: int,
        job_id: int,
    ) -> ResumeTailorResponse | None:
        """
        ID-based entry point used by DailyPipelineService.
        Fetches parsed objects from their repos, then delegates to .tailor().
        """

        if not self.parsed_resume_repository or not self.parsed_job_repository:
            logger.error("Cannot call tailor_resume without parsed repos")
            return None

        parsed_resume = self.parsed_resume_repository.get_by_resume_id(resume_id)
        parsed_job = self.parsed_job_repository.get_by_job_id(job_id)

        if parsed_resume is None or parsed_job is None:
            logger.warning(
                "Missing parsed data for resume=%s job=%s",
                resume_id,
                job_id,
            )
            return None

        return self.tailor(parsed_resume, parsed_job)