from sqlalchemy.orm import Session

from backend.app.models.tailored_resume import TailoredResume


class TailoredResumeRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        tailored_resume: TailoredResume,
    ) -> TailoredResume:

        self.db.add(tailored_resume)
        self.db.commit()
        self.db.refresh(tailored_resume)

        return tailored_resume

    def update(
        self,
        tailored_resume: TailoredResume,
    ) -> TailoredResume:

        self.db.commit()
        self.db.refresh(tailored_resume)

        return tailored_resume

    def get(
        self,
        resume_id: int,
        job_id: int,
    ) -> TailoredResume | None:

        return (
            self.db.query(TailoredResume)
            .filter(
                TailoredResume.resume_id == resume_id,
                TailoredResume.job_id == job_id,
            )
            .first()
        )

    def delete(
        self,
        tailored_resume: TailoredResume,
    ):

        self.db.delete(
            tailored_resume
        )

        self.db.commit()