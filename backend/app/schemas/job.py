from datetime import datetime

from pydantic import BaseModel, ConfigDict


class JobCreate(BaseModel):
    title: str | None = None
    company: str | None = None
    location: str | None = None
    source: str | None = None
    job_url: str | None = None
    raw_text: str


class JobResponse(BaseModel):
    id: int
    user_id: int
    title: str | None = None
    company: str | None = None
    location: str | None = None
    source: str | None = None
    job_url: str | None = None
    raw_text: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )