from backend.app.models.job_description import JobDescription
from backend.app.models.user import User
from backend.app.repositories.job_repository import JobRepository
from backend.app.services.parsed_job_service import ParsedJobService


class JobService:

    def __init__(
        self,
        repository: JobRepository,
        parsed_service: ParsedJobService | None = None,
    ):
        self.repository = repository
        self.parsed_service = parsed_service

    def create_job(
        self,
        current_user: User,
        job_data,
    ) -> JobDescription:

        job = JobDescription(
            user_id=current_user.id,
            title=job_data.title,
            company=job_data.company,
            location=job_data.location,
            source=job_data.source,
            job_url=job_data.job_url,
            raw_text=job_data.raw_text,
        )

        return self.repository.create(job)

    def get_jobs(
        self,
        current_user: User,
    ):

        return self.repository.get_by_user(
            current_user.id
        )

    def get_job(
        self,
        job_id: int,
    ):

        return self.repository.get_by_id(
            job_id
        )

    def delete_job(
        self,
        job: JobDescription,
    ):

        return self.repository.delete(
            job
        )

    def parse_job(
        self,
        job: JobDescription,
    ):

        return self.parsed_service.parse_job(
            job
        )