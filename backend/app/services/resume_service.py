from pathlib import Path

from backend.app.models.parsed_resume import ParsedResume
from backend.app.models.resume import Resume
from backend.app.models.user import User
from backend.app.repositories.parsed_resume_repository import (
    ParsedResumeRepository,
)
from backend.app.repositories.resume_repository import ResumeRepository
from backend.app.schemas.resume import ResumeCreate
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

        return self.repository.create(resume)

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

        raw_text = ResumeParserService.extract_text(
            resume.file_path
        )

        sections = ResumeSectionExtractor.extract_sections(
            raw_text
        )

        skills = ResumeIntelligenceService.extract_skills(
            sections["skills"]
        )

        parsed_resume = self.parsed_repository.get_by_resume_id(
            resume.id
        )

        if parsed_resume:

            parsed_resume.raw_text = raw_text
            parsed_resume.skills = skills
            parsed_resume.experience = sections["experience"]
            parsed_resume.education = sections["education"]
            parsed_resume.projects = sections["projects"]
            parsed_resume.certifications = sections["certifications"]

            return self.parsed_repository.update(
                parsed_resume
            )

        parsed_resume = ParsedResume(
            resume_id=resume.id,
            raw_text=raw_text,
            skills=skills,
            experience=sections["experience"],
            education=sections["education"],
            projects=sections["projects"],
            certifications=sections["certifications"],
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

        return ATSScoreService.calculate(
            parsed_resume
        )