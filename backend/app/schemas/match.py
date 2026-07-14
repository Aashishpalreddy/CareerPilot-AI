from pydantic import BaseModel


class MatchResponse(BaseModel):
    resume_id: int
    job_id: int

    match_score: float

    matched_skills: list[str]
    missing_skills: list[str]

    recommendations: list[str]