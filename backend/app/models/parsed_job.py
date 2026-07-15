from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.session import Base


class ParsedJob(Base):
    __tablename__ = "parsed_jobs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    job_id: Mapped[int] = mapped_column(
        ForeignKey(
            "job_descriptions.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
    )

    raw_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    title: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    company: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    location: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    employment_type: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    job_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    skills: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    preferred_skills: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    technologies: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    responsibilities: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    qualifications: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    experience: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    education: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    certifications: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    soft_skills: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    keywords: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    parsed_json: Mapped[dict | None] = mapped_column(
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

    job = relationship(
        "JobDescription",
        back_populates="parsed_job",
    )