from sqlalchemy.orm import Session

from backend.app.models.cover_letter import CoverLetter


class CoverLetterRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        cover_letter: CoverLetter,
    ) -> CoverLetter:

        self.db.add(cover_letter)
        self.db.commit()
        self.db.refresh(cover_letter)

        return cover_letter

    def update(
        self,
        cover_letter: CoverLetter,
    ) -> CoverLetter:

        self.db.commit()
        self.db.refresh(cover_letter)

        return cover_letter

    def get(
        self,
        resume_id: int,
        job_id: int,
    ) -> CoverLetter | None:

        return (
            self.db.query(CoverLetter)
            .filter(
                CoverLetter.resume_id == resume_id,
                CoverLetter.job_id == job_id,
            )
            .first()
        )

    def get_by_id(
        self,
        cover_letter_id: int,
    ) -> CoverLetter | None:

        return (
            self.db.query(CoverLetter)
            .filter(
                CoverLetter.id == cover_letter_id,
            )
            .first()
        )

    def delete(
        self,
        cover_letter: CoverLetter,
    ):

        self.db.delete(
            cover_letter
        )

        self.db.commit()