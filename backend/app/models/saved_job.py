from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.session import Base


class SavedJob(Base):
    """
    A job the daily pipeline discovered, matched against the user's resume,
    and pre-generated apply materials for. This is what "Apply Now" reads
    from, so the click-to-apply step is just a lookup instead of a fresh
    round of AI generation.
    """

    __tablename__ = "saved_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    job_id: Mapped[int] = mapped_column(
        ForeignKey("job_descriptions.id", ondelete="CASCADE"),
        nullable=False,
    )

    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False,
    )

    match_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    tailored_resume_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    cover_letter_text: Mapped[str | None] = mapped_column(Text, nullable=True)

    apply_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    # True only for direct company/ATS application links. LinkedIn, Indeed,
    # and Handshake jobs are always False - those are hand-off-only links.
    auto_apply_eligible: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    recruiter_links: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # saved -> pending review, applied -> user clicked apply / confirmed
    # submission, skipped -> user dismissed it, failed -> auto-apply attempt
    # failed and fell back to a manual link
    status: Mapped[str] = mapped_column(
        String(20),
        default="saved",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
    )

    applied_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    job = relationship("JobDescription")
    resume = relationship("Resume")
