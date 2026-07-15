from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.session import Base


class TailoredResume(Base):
    __tablename__ = "tailored_resumes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    resume_id: Mapped[int] = mapped_column(
        ForeignKey(
            "resumes.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    job_id: Mapped[int] = mapped_column(
        ForeignKey(
            "job_descriptions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    tailored_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    tailored_experience: Mapped[list[Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    tailored_projects: Mapped[list[Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    ats_keywords: Mapped[list[Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    overall_match: Mapped[float | None] = mapped_column(
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    resume = relationship(
    "Resume",
    back_populates="tailored_resumes",
    )

    job = relationship(
    "JobDescription",
    back_populates="tailored_resumes",
    )