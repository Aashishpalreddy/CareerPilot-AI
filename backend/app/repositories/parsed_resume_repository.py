from sqlalchemy.orm import Session

from backend.app.models.parsed_resume import ParsedResume


class ParsedResumeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, parsed_resume: ParsedResume) -> ParsedResume:
        self.db.add(parsed_resume)
        self.db.commit()
        self.db.refresh(parsed_resume)
        return parsed_resume

    def get_by_resume_id(self, resume_id: int) -> ParsedResume | None:
        return (
            self.db.query(ParsedResume)
            .filter(ParsedResume.resume_id == resume_id)
            .first()
        )

    def update(self, parsed_resume: ParsedResume) -> ParsedResume:
        self.db.commit()
        self.db.refresh(parsed_resume)
        return parsed_resume

    def delete(self, parsed_resume: ParsedResume) -> None:
        self.db.delete(parsed_resume)
        self.db.commit()