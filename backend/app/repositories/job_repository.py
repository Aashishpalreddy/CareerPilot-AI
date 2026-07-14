from sqlalchemy.orm import Session

from backend.app.models.job_description import JobDescription


class JobRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        job: JobDescription,
    ) -> JobDescription:

        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)

        return job

    def get_by_id(
        self,
        job_id: int,
    ) -> JobDescription | None:

        return (
            self.db.query(JobDescription)
            .filter(JobDescription.id == job_id)
            .first()
        )

    def get_by_user(
        self,
        user_id: int,
    ):

        return (
            self.db.query(JobDescription)
            .filter(JobDescription.user_id == user_id)
            .order_by(JobDescription.created_at.desc())
            .all()
        )

    def delete(
        self,
        job: JobDescription,
    ):

        self.db.delete(job)
        self.db.commit()