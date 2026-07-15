from pydantic import BaseModel


class GeneratedResumeResponse(BaseModel):
    resume_id: int
    job_id: int

    output_path: str

    download_url: str