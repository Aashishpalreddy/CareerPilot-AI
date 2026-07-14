from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import ARRAY

from backend.app.database.base import Base


class MatchResult(Base):
    __tablename__ = "match_results"

    id = Column(Integer, primary_key=True, index=True)

    resume_id = Column(
        Integer,
        ForeignKey("resumes.id"),
        nullable=False,
    )

    job_id = Column(
        Integer,
        ForeignKey("job_descriptions.id"),
        nullable=False,
    )

    match_score = Column(
        Float,
        nullable=False,
    )

    matched_skills = Column(
        ARRAY(str),
        nullable=False,
    )

    missing_skills = Column(
        ARRAY(str),
        nullable=False,
    )