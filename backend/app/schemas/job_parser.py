from typing import Optional, List, Dict, Any

from pydantic import BaseModel, ConfigDict


class JobParserResponse(BaseModel):
    job_title: Optional[str] = None

    company: Optional[str] = None

    location: Optional[str] = None

    employment_type: Optional[str] = None

    summary: Optional[str] = None

    required_skills: List[str] = []

    preferred_skills: List[str] = []

    technologies: List[str] = []

    responsibilities: List[str] = []

    qualifications: List[str] = []

    experience: List[str] = []

    education: List[str] = []

    certifications: List[str] = []

    soft_skills: List[str] = []

    keywords: List[str] = []

    salary: Optional[str] = None

    benefits: List[str] = []

    parsed_json: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(
        from_attributes=True,
    )


class JobParseRequest(BaseModel):
    job_id: int


class JobDescriptionCreate(BaseModel):
    title: Optional[str] = None

    company: Optional[str] = None

    location: Optional[str] = None

    source: Optional[str] = None

    job_url: Optional[str] = None

    raw_text: str


class JobDescriptionResponse(BaseModel):

    id: int

    user_id: int

    title: Optional[str] = None

    company: Optional[str] = None

    location: Optional[str] = None

    source: Optional[str] = None

    job_url: Optional[str] = None

    raw_text: str

    model_config = ConfigDict(
        from_attributes=True,
    )