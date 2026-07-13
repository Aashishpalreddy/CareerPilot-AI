from backend.app.models.resume import Resume
from backend.app.models.user import User
from backend.app.repositories.resume_repository import ResumeRepository
from backend.app.schemas.resume import ResumeCreate


class ResumeService:
    """Business logic for resume management."""

    def __init__(self, repository: ResumeRepository):
        self.repository = repository

    def create_resume(
        self,
        user: User,
        resume_data: ResumeCreate,
    ) -> Resume:
        resume = Resume(
            user_id=user.id,
            title=resume_data.title,
            original_filename=resume_data.original_filename,
            file_path=resume_data.file_path,
        )

        return self.repository.create(resume)

    def get_resumes(
        self,
        user: User,
    ) -> list[Resume]:
        return self.repository.get_all_by_user(user.id)

    def get_resume(
        self,
        resume_id: int,
    ) -> Resume | None:
        return self.repository.get_by_id(resume_id)

    def delete_resume(
        self,
        resume: Resume,
    ) -> None:
        self.repository.delete(resume)