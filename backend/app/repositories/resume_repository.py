from sqlalchemy.orm import Session

from backend.app.models.resume import Resume


class ResumeRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, resume: Resume):
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)
        return resume

    def get_by_user(self, user_id: int):
        return (
            self.db.query(Resume)
            .filter(Resume.user_id == user_id)
            .all()
        )

    def get_by_id(self, resume_id: int):
        return (
            self.db.query(Resume)
            .filter(Resume.id == resume_id)
            .first()
        )

    def get_default(self, user_id: int):
        return (
            self.db.query(Resume)
            .filter(
                Resume.user_id == user_id,
                Resume.is_default.is_(True),
            )
            .first()
        )

    def delete(self, resume: Resume):
        self.db.delete(resume)
        self.db.commit()

    def unset_default(self, user_id: int):
        self.db.query(Resume).filter(
            Resume.user_id == user_id
        ).update(
            {
                Resume.is_default: False
            }
        )

        self.db.commit()

    def set_default(self, resume: Resume):
        resume.is_default = True
        self.db.commit()
        self.db.refresh(resume)

        return resume