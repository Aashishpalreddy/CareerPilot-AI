from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ParsedJobResponse(BaseModel):
    id: int
    job_id: int

    raw_text: str

    title: str | None = None
    company: str | None = None

    skills: list[Any] | None = None
    responsibilities: list[Any] | None = None
    qualifications: list[Any] | None = None
    experience: list[Any] | None = None
    education: list[Any] | None = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )