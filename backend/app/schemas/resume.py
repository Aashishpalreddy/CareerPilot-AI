from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResumeCreate(BaseModel):
    title: str
    original_filename: str
    file_path: str


class ResumeResponse(BaseModel):
    id: int
    user_id: int
    title: str
    original_filename: str
    file_path: str
    is_default: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)