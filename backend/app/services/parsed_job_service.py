from backend.app.models.job_description import JobDescription
from backend.app.models.parsed_job import ParsedJob

from backend.app.repositories.parsed_job_repository import (
    ParsedJobRepository,
)

from backend.app.services.ai_job_parser import AIJobParser
from backend.app.services.job_parser_service import JobParserService


class ParsedJobService:

    def __init__(
        self,
        repository: ParsedJobRepository,
    ):

        self.repository = repository
        self.ai_parser = AIJobParser()


    def parse_job(
        self,
        job: JobDescription,
    ) -> ParsedJob:

        try:
            # Primary parser: Claude AI
            parsed_response = self.ai_parser.parse(
                job.raw_text
            )

            parsed = parsed_response.model_dump()


        except Exception as e:

            print(
                "AI JOB PARSER FAILED:",
                str(e)
            )

            # Fallback parser: Rule based
            parsed = JobParserService.parse(
                job.raw_text
            )


        existing = self.repository.get_by_job_id(
            job.id
        )


        if existing:

            existing.raw_text = job.raw_text

            existing.title = (
                job.title
                or parsed.get("job_title")
                or parsed.get("title")
            )

            existing.company = (
                job.company
                or parsed.get("company")
            )

            existing.location = (
                job.location
                or parsed.get("location")
            )

            existing.employment_type = (
                parsed.get("employment_type")
            )

            existing.job_summary = (
                parsed.get("summary")
            )

            existing.skills = (
                parsed.get("required_skills")
                or parsed.get("skills")
            )

            existing.preferred_skills = (
                parsed.get("preferred_skills")
            )

            existing.technologies = (
                parsed.get("technologies")
            )

            existing.responsibilities = (
                parsed.get("responsibilities")
            )

            existing.qualifications = (
                parsed.get("qualifications")
            )

            existing.experience = (
                parsed.get("experience")
            )

            existing.education = (
                parsed.get("education")
            )

            existing.certifications = (
                parsed.get("certifications")
            )

            existing.soft_skills = (
                parsed.get("soft_skills")
            )

            existing.keywords = (
                parsed.get("keywords")
            )

            existing.parsed_json = parsed


            return self.repository.update(
                existing
            )


        parsed_job = ParsedJob(

            job_id=job.id,

            raw_text=job.raw_text,

            title=(
                job.title
                or parsed.get("job_title")
                or parsed.get("title")
            ),

            company=(
                job.company
                or parsed.get("company")
            ),

            location=(
                job.location
                or parsed.get("location")
            ),

            employment_type=(
                parsed.get("employment_type")
            ),

            job_summary=(
                parsed.get("summary")
            ),

            skills=(
                parsed.get("required_skills")
                or parsed.get("skills")
            ),

            preferred_skills=(
                parsed.get("preferred_skills")
            ),

            technologies=(
                parsed.get("technologies")
            ),

            responsibilities=(
                parsed.get("responsibilities")
            ),

            qualifications=(
                parsed.get("qualifications")
            ),

            experience=(
                parsed.get("experience")
            ),

            education=(
                parsed.get("education")
            ),

            certifications=(
                parsed.get("certifications")
            ),

            soft_skills=(
                parsed.get("soft_skills")
            ),

            keywords=(
                parsed.get("keywords")
            ),

            parsed_json=parsed,
        )


        return self.repository.create(
            parsed_job
        )