from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ParsedResumeResponse(BaseModel):
    id: int
    resume_id: int

    raw_text: str

    summary: str | None = None

    skills: list[str] | None = None

    experience: list[Any] | None = None

    education: list[Any] | None = None

    projects: list[Any] | None = None

    certifications: list[Any] | None = None

    technologies: list[str] | None = None

    languages: list[str] | None = None

    achievements: list[str] | None = None

    years_experience: float | None = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )