from pydantic import BaseModel

from backend.app.schemas.keyword_gap import MatchResult


class ResumeMatchResponse(BaseModel):
    overall_match: float

    fit_level: str

    recommendation: str

    skills: MatchResult

    technologies: MatchResult

    certifications: MatchResult

    experience_match: bool

    education_match: bool