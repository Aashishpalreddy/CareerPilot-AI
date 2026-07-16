from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Float, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.session import Base


class ParsedResume(Base):
    __tablename__ = "parsed_resumes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    raw_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    skills: Mapped[list[Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    experience: Mapped[list[Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    education: Mapped[list[Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    projects: Mapped[list[Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    certifications: Mapped[list[Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    technologies: Mapped[list[Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    languages: Mapped[list[Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    achievements: Mapped[list[Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    years_experience: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    ats_score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    ats_strengths: Mapped[list[Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    ats_weaknesses: Mapped[list[Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    ats_suggestions: Mapped[list[Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    resume = relationship(
        "Resume",
        back_populates="parsed_resume",
    )