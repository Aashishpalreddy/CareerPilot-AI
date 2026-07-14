from dataclasses import dataclass


@dataclass
class RoleMatchResult:
    matched: bool
    score: int
    matched_role: str | None
    reason: str


class JobRoleMatcher:
    """
    Determines whether a job title is relevant for
    Software / AI / ML careers.
    """

    ROLE_SCORES = {
        # AI
        "ai engineer": 100,
        "artificial intelligence engineer": 100,
        "machine learning engineer": 100,
        "ml engineer": 100,
        "deep learning engineer": 100,
        "llm engineer": 100,
        "generative ai engineer": 100,
        "genai engineer": 100,
        "applied ai engineer": 100,
        "ai developer": 95,

        # Data
        "data scientist": 95,
        "data engineer": 95,
        "analytics engineer": 90,
        "data analyst": 80,

        # Software
        "software engineer": 95,
        "software developer": 95,
        "backend engineer": 95,
        "backend developer": 95,
        "frontend engineer": 90,
        "frontend developer": 90,
        "full stack engineer": 95,
        "full stack developer": 95,

        # Python
        "python developer": 95,
        "python engineer": 95,

        # Cloud
        "cloud engineer": 85,
        "devops engineer": 85,
        "site reliability engineer": 85,

        # Security
        "security engineer": 80,
        "cybersecurity engineer": 80,
    }

    @classmethod
    def match(cls, title: str) -> RoleMatchResult:

        title = title.lower().strip()

        best_score = 0
        best_role = None

        for role, score in cls.ROLE_SCORES.items():

            if role in title:

                if score > best_score:
                    best_score = score
                    best_role = role

        if best_role:

            return RoleMatchResult(
                matched=True,
                score=best_score,
                matched_role=best_role,
                reason=f"Matched '{best_role}'",
            )

        return RoleMatchResult(
            matched=False,
            score=0,
            matched_role=None,
            reason="Job title is not a software/AI role.",
        )