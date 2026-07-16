from sqlalchemy.orm import Session

from backend.app.models.job_description import JobDescription
from backend.app.models.saved_job import SavedJob


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

    def get_by_user_and_url(
        self,
        user_id: int,
        job_url: str | None,
    ) -> JobDescription | None:

        if not job_url:
            return None

        return (
            self.db.query(JobDescription)
            .filter(
                JobDescription.user_id == user_id,
                JobDescription.job_url == job_url,
            )
            .first()
        )

    def delete(
        self,
        job: JobDescription,
    ):

        self.db.delete(job)
        self.db.commit()

    def delete_discovered_for_user(
        self,
        user_id: int,
    ) -> int:
        """
        Removes previously auto-discovered jobs for a user so a new search
        replaces the tracked-jobs list instead of piling on top of it.
        Manually-added jobs (source is null) and any job already tailored/
        applied to (has a SavedJob) are left alone.
        """

        saved_job_ids = (
            self.db.query(SavedJob.job_id)
            .filter(SavedJob.user_id == user_id)
            .subquery()
        )

        deleted = (
            self.db.query(JobDescription)
            .filter(
                JobDescription.user_id == user_id,
                JobDescription.source.isnot(None),
                JobDescription.id.notin_(saved_job_ids),
            )
            .delete(synchronize_session=False)
        )

        self.db.commit()
        return deleted