from pydantic import BaseModel, Field, field_validator, model_validator


def _coerce_description(value) -> str:
    """LLMs commonly return bullet points as a list of strings; normalize any
    list / None into a single newline-joined string."""
    if value is None:
        return ""
    if isinstance(value, list):
        return "\n".join(str(item).strip() for item in value if item is not None)
    return str(value)


class Experience(BaseModel):
    company: str = ""
    title: str = ""
    location: str = ""
    start_date: str = ""
    end_date: str = ""
    description: str = ""

    _norm_description = field_validator("description", mode="before")(
        _coerce_description
    )


class Education(BaseModel):
    institution: str = ""
    degree: str = ""
    field_of_study: str = ""
    start_date: str = ""
    end_date: str = ""


class Project(BaseModel):
    name: str = ""
    description: str = ""
    technologies: list[str] = Field(default_factory=list)

    _norm_description = field_validator("description", mode="before")(
        _coerce_description
    )


class Certification(BaseModel):
    name: str = ""
    issuer: str = ""
    issue_date: str = ""

    @model_validator(mode="before")
    @classmethod
    def _accept_plain_string(cls, value):
        # LLMs sometimes return certifications as plain strings rather than
        # objects; wrap a bare string as {"name": ...}.
        if isinstance(value, str):
            return {"name": value}
        return value


class ResumeProfile(BaseModel):
    summary: str = ""

    skills: list[str] = Field(default_factory=list)

    experience: list[Experience] = Field(default_factory=list)

    education: list[Education] = Field(default_factory=list)

    projects: list[Project] = Field(default_factory=list)

    certifications: list[Certification] = Field(default_factory=list)

    technologies: list[str] = Field(default_factory=list)

    languages: list[str] = Field(default_factory=list)

    achievements: list[str] = Field(default_factory=list)

    years_experience: float = 0