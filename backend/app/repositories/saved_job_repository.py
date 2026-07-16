from datetime import datetime, timezone

from sqlalchemy.orm import Session, joinedload

from backend.app.models.saved_job import SavedJob


class SavedJobRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, saved_job: SavedJob) -> SavedJob:
        self.db.add(saved_job)
        self.db.commit()
        self.db.refresh(saved_job)
        return saved_job

    def get_by_id(self, saved_job_id: int) -> SavedJob | None:
        return (
            self.db.query(SavedJob)
            .options(joinedload(SavedJob.job))
            .filter(SavedJob.id == saved_job_id)
            .first()
        )

    def get_by_user_and_job(
        self,
        user_id: int,
        job_id: int,
    ) -> SavedJob | None:
        return (
            self.db.query(SavedJob)
            .filter(
                SavedJob.user_id == user_id,
                SavedJob.job_id == job_id,
            )
            .first()
        )

    def get_by_user(
        self,
        user_id: int,
        status: str | None = None,
    ) -> list[SavedJob]:
        query = (
            self.db.query(SavedJob)
            .options(joinedload(SavedJob.job))
            .filter(SavedJob.user_id == user_id)
        )

        if status:
            query = query.filter(SavedJob.status == status)

        return query.order_by(SavedJob.created_at.desc()).all()

    def update(self, saved_job: SavedJob) -> SavedJob:
        self.db.commit()
        self.db.refresh(saved_job)
        return saved_job

    def mark_applied(self, saved_job: SavedJob) -> SavedJob:
        saved_job.status = "applied"
        saved_job.applied_at = datetime.now(timezone.utc)
        return self.update(saved_job)

    def delete(self, saved_job: SavedJob) -> None:
        self.db.delete(saved_job)
        self.db.commit()
