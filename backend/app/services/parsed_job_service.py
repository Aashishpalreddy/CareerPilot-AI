from backend.app.models.job_description import JobDescription
from backend.app.models.parsed_job import ParsedJob
from backend.app.repositories.parsed_job_repository import (
    ParsedJobRepository,
)
from backend.app.services.job_parser_service import JobParserService


class ParsedJobService:

    def __init__(
        self,
        repository: ParsedJobRepository,
    ):
        self.repository = repository

    def parse_job(
        self,
        job: JobDescription,
    ) -> ParsedJob:

        parsed = JobParserService.parse(
            job.raw_text
        )

        existing = self.repository.get_by_job_id(
            job.id
        )

        if existing:

            existing.raw_text = job.raw_text

            # Use metadata from the provider instead of parsing HTML
            existing.title = job.title
            existing.company = job.company

            existing.skills = parsed["skills"]
            existing.experience = parsed["experience"]
            existing.education = parsed["education"]
            existing.responsibilities = parsed["responsibilities"]
            existing.qualifications = parsed["qualifications"]

            return self.repository.update(
                existing
            )

        parsed_job = ParsedJob(
            job_id=job.id,
            raw_text=job.raw_text,

            # Use metadata from the provider instead of parsing HTML
            title=job.title,
            company=job.company,

            skills=parsed["skills"],
            experience=parsed["experience"],
            education=parsed["education"],
            responsibilities=parsed["responsibilities"],
            qualifications=parsed["qualifications"],
        )

        return self.repository.create(
            parsed_job
        )