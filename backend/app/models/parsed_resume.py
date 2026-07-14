from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Integer, Text
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