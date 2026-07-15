from typing import List

from pydantic import BaseModel


class MatchResult(BaseModel):
    matched: List[str]
    missing: List[str]
    score: float


class KeywordGapResponse(BaseModel):
    overall_score: float

    skills: MatchResult

    technologies: MatchResult

    certifications: MatchResult

    experience_match: bool

    education_match: bool

    recommendations: List[str]