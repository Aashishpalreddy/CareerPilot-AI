from pydantic import BaseModel


class TailoredBullet(BaseModel):
    section: str
    bullet: str


class ResumeTailorResponse(BaseModel):
    resume_id: int
    job_id: int

    original_match_score: float
    improved_match_score: float

    tailored_summary: str

    tailored_experience: list[dict]
    tailored_projects: list[dict]

    ats_keywords: list[str]

    tailored_bullets: list[TailoredBullet]

    keywords_added: list[str]
    keywords_missing: list[str]