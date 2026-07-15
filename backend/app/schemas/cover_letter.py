from datetime import datetime

from pydantic import BaseModel


class CoverLetterGenerateResponse(BaseModel):
    cover_letter_text: str


class CoverLetterResponse(BaseModel):
    id: int

    resume_id: int
    job_id: int

    company: str
    position: str

    content: str

    docx_filename: str | None = None
    pdf_filename: str | None = None

    status: str

    created_at: datetime

    model_config = {
        "from_attributes": True
    }