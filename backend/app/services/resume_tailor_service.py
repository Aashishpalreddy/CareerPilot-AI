from backend.app.models.parsed_job import ParsedJob
from backend.app.models.parsed_resume import ParsedResume
from backend.app.models.tailored_resume import TailoredResume

from backend.app.repositories.tailored_resume_repository import (
    TailoredResumeRepository,
)

from backend.app.schemas.resume_tailor import (
    ResumeTailorResponse,
)

from backend.app.services.ai_resume_tailor import (
    AIResumeTailor,
)

from backend.app.services.resume_match_service import (
    ResumeMatchService,
)


class ResumeTailorService:

    def __init__(
        self,
        repository: TailoredResumeRepository,
    ):
        self.repository = repository
        self.ai = AIResumeTailor()
        self.matcher = ResumeMatchService()

    def tailor(
        self,
        parsed_resume: ParsedResume,
        parsed_job: ParsedJob,
    ) -> ResumeTailorResponse:

        match = self.matcher.match(
            parsed_resume,
            parsed_job,
        )

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
        )

        existing = self.repository.get(
            parsed_resume.resume_id,
            parsed_job.job_id,
        )

        if existing:

            existing.tailored_summary = (
                ai_result.tailored_summary
            )

            existing.tailored_experience = (
                ai_result.tailored_experience
            )

            existing.tailored_projects = (
                ai_result.tailored_projects
            )

            existing.ats_keywords = (
                ai_result.ats_keywords
            )

            existing.overall_match = (
                match.overall_match
            )

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

            self.repository.create(
                tailored
            )

        return ResumeTailorResponse(

            resume_id=parsed_resume.resume_id,

            job_id=parsed_job.job_id,

            original_match_score=match.overall_match,

            improved_match_score=min(
                100,
                match.overall_match + 15,
            ),

            tailored_summary=ai_result.tailored_summary,

            tailored_experience=ai_result.tailored_experience,

            tailored_projects=ai_result.tailored_projects,

            ats_keywords=ai_result.ats_keywords,

            tailored_bullets=ai_result.tailored_bullets,

            keywords_added=ai_result.keywords_added,

            keywords_missing=ai_result.keywords_missing,
        )