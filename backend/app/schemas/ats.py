from pydantic import BaseModel


class ATSScoreResponse(BaseModel):
    score: int
    strengths: list[str]
    weaknesses: list[str]
    suggestions: list[str]