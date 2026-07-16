from pathlib import Path

from backend.app.models.parsed_resume import ParsedResume
from backend.app.models.resume import Resume
from backend.app.models.user import User
from backend.app.repositories.parsed_resume_repository import (
    ParsedResumeRepository,
)
from backend.app.repositories.resume_repository import ResumeRepository
from backend.app.schemas.resume import ResumeCreate
from backend.app.services.ai_resume_parser import AIResumeParser
from backend.app.services.ats_score_service import ATSScoreService
from backend.app.services.resume_intelligence_service import (
    ResumeIntelligenceService,
)
from backend.app.services.resume_parser_service import ResumeParserService
from backend.app.services.resume_section_extractor import (
    ResumeSectionExtractor,
)


class ResumeService:

    def __init__(
        self,
        repository: ResumeRepository,
        parsed_repository: ParsedResumeRepository,
    ):
        self.repository = repository
        self.parsed_repository = parsed_repository
        self.ai_parser = AIResumeParser()

    def create_resume(
        self,
        current_user: User,
        resume_data: ResumeCreate,
    ) -> Resume:

        resume = Resume(
            user_id=current_user.id,
            title=resume_data.title,
            original_filename=resume_data.original_filename,
            file_path=resume_data.file_path,
            is_default=False,
        )

        created = self.repository.create(resume)
        self.set_default_resume(current_user, created)
        return created

    def get_resumes(self, current_user: User):
        return self.repository.get_by_user(current_user.id)

    def get_resume(self, resume_id: int):
        return self.repository.get_by_id(resume_id)

    def delete_resume(self, resume: Resume):

        if resume.file_path:
            file_path = Path(resume.file_path)

            if file_path.exists():
                file_path.unlink()

        return self.repository.delete(resume)

    def set_default_resume(
        self,
        current_user: User,
        resume: Resume,
    ):

        self.repository.unset_default(
            current_user.id
        )

        return self.repository.set_default(resume)

    def parse_resume(
        self,
        resume: Resume,
    ) -> ParsedResume:

        try:
            raw_text = ResumeParserService.extract_text(resume.file_path)
            sections = ResumeSectionExtractor.extract_sections(raw_text)
            skills = ResumeIntelligenceService.extract_skills(sections["skills"])
        except Exception as e:
            import logging
            logging.getLogger(__name__).exception(f"Basic parsing failed: {e}")
            raise ValueError(f"Failed to parse resume file: {e}")

        ai_profile = None

        try:
            ai_profile = self.ai_parser.parse(raw_text)
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"AI parsing failed, falling back to basic parsing. Error: {e}")
            # Keep existing parsing if AI fails
            ai_profile = None

        parsed_resume = self.parsed_repository.get_by_resume_id(resume.id)

        if parsed_resume is None:

            parsed_resume = ParsedResume(
                resume_id=resume.id,
                raw_text=raw_text,
            )

        parsed_resume.raw_text = raw_text

        if ai_profile:

            parsed_resume.summary = ai_profile.summary
            parsed_resume.skills = ai_profile.skills

            parsed_resume.experience = [
                exp.model_dump()
                for exp in ai_profile.experience
            ]

            parsed_resume.education = [
                edu.model_dump()
                for edu in ai_profile.education
            ]

            parsed_resume.projects = [
                project.model_dump()
                for project in ai_profile.projects
            ]

            parsed_resume.certifications = [
                cert.model_dump()
                for cert in ai_profile.certifications
            ]

            parsed_resume.technologies = ai_profile.technologies
            parsed_resume.languages = ai_profile.languages
            parsed_resume.achievements = ai_profile.achievements
            parsed_resume.years_experience = (
                ai_profile.years_experience
            )

        else:

            parsed_resume.summary = None
            parsed_resume.skills = skills
            parsed_resume.experience = sections["experience"]
            parsed_resume.education = sections["education"]
            parsed_resume.projects = sections["projects"]
            parsed_resume.certifications = (
                sections["certifications"]
            )
            parsed_resume.technologies = []
            parsed_resume.languages = []
            parsed_resume.achievements = []
            parsed_resume.years_experience = 0

        if parsed_resume.id:
            return self.parsed_repository.update(
                parsed_resume
            )

        return self.parsed_repository.create(
            parsed_resume
        )

    def get_ats_score(
        self,
        resume: Resume,
    ):
        parsed_resume = self.parsed_repository.get_by_resume_id(
            resume.id
        )

        if parsed_resume is None:
            parsed_resume = self.parse_resume(
                resume
            )

        # Return cached score if it exists
        if parsed_resume.ats_score is not None:
            return {
                "score": parsed_resume.ats_score,
                "strengths": parsed_resume.ats_strengths or [],
                "weaknesses": parsed_resume.ats_weaknesses or [],
                "suggestions": parsed_resume.ats_suggestions or [],
            }

        # Calculate if not cached
        ats_data = ATSScoreService.calculate(
            parsed_resume
        )
        
        # Avoid caching the fallback error data so it can be retried later when API rate limit resets
        is_fallback = (
            ats_data.get("strengths") == ["Could not analyze properly due to an error."] or 
            (ats_data.get("strengths") and "Resume is well structured and parsable by ATS." in ats_data.get("strengths")[0])
        )
        
        if not is_fallback:
            parsed_resume.ats_score = ats_data.get("score")
            parsed_resume.ats_strengths = ats_data.get("strengths")
            parsed_resume.ats_weaknesses = ats_data.get("weaknesses")
            parsed_resume.ats_suggestions = ats_data.get("suggestions")
            self.parsed_repository.update(parsed_resume)

        return ats_data