from pathlib import Path

from backend.app.models.resume import Resume
from backend.app.models.user import User
from backend.app.repositories.resume_repository import ResumeRepository
from backend.app.schemas.resume import ResumeCreate


class ResumeService:

    def __init__(self, repository: ResumeRepository):
        self.repository = repository

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