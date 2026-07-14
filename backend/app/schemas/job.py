from datetime import datetime

from pydantic import BaseModel, ConfigDict


class JobCreate(BaseModel):
    raw_text: str


class JobResponse(BaseModel):
    id: int
    user_id: int
    raw_text: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )