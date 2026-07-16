from datetime import datetime

from pydantic import BaseModel, ConfigDict


class JobInfo(BaseModel):
    """Lightweight nested view of the related JobDescription."""

    id: int
    title: str | None = None
    company: str | None = None
    location: str | None = None
    source: str | None = None
    job_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class SavedJobResponse(BaseModel):
    id: int
    user_id: int
    job_id: int
    resume_id: int

    match_score: float | None = None

    tailored_resume_text: str | None = None
    cover_letter_text: str | None = None

    apply_url: str | None = None
    auto_apply_eligible: bool

    recruiter_links: dict | None = None

    status: str

    created_at: datetime
    applied_at: datetime | None = None

    job: JobInfo | None = None

    model_config = ConfigDict(from_attributes=True)


class SavedJobSummary(BaseModel):
    """Lightweight view for list screens — no generated text bodies."""

    id: int
    job_id: int
    match_score: float | None = None
    apply_url: str | None = None
    auto_apply_eligible: bool
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
