from backend.app.repositories.parsed_resume_repository import ParsedResumeRepository
from backend.app.repositories.parsed_job_repository import ParsedJobRepository
from backend.app.schemas.resume_tailor import ResumeTailorResponse


class ResumeTailorService:

    def __init__(
        self,
        parsed_resume_repository: ParsedResumeRepository,
        parsed_job_repository: ParsedJobRepository,
    ):
        self.parsed_resume_repository = parsed_resume_repository
        self.parsed_job_repository = parsed_job_repository

    def tailor_resume(
        self,
        resume_id: int,
        job_id: int,
    ):
        pass