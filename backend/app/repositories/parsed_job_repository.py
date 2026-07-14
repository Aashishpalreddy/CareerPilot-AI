from sqlalchemy.orm import Session

from backend.app.models.parsed_job import ParsedJob


class ParsedJobRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        parsed_job: ParsedJob,
    ) -> ParsedJob:

        self.db.add(parsed_job)
        self.db.commit()
        self.db.refresh(parsed_job)

        return parsed_job

    def update(
        self,
        parsed_job: ParsedJob,
    ) -> ParsedJob:

        self.db.commit()
        self.db.refresh(parsed_job)

        return parsed_job

    def get_by_job_id(
        self,
        job_id: int,
    ) -> ParsedJob | None:

        return (
            self.db.query(ParsedJob)
            .filter(
                ParsedJob.job_id == job_id
            )
            .first()
        )