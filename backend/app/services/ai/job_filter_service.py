from dataclasses import dataclass
import re


@dataclass
class FilterResult:
    accepted: bool
    confidence: float
    score: int
    reason: str


class JobFilterService:

    ALLOWED_TITLES = {
        "software engineer",
        "software developer",
        "backend engineer",
        "backend developer",
        "backend software engineer",
        "python developer",
        "python engineer",
        "ai engineer",
        "artificial intelligence engineer",
        "machine learning engineer",
        "ml engineer",
        "data engineer",
        "data scientist",
        "llm engineer",
        "nlp engineer",
        "computer vision engineer",
        "generative ai engineer",
        "full stack developer",
        "full stack engineer",
        "devops engineer",
        "cloud engineer",
        "site reliability engineer",
        "platform engineer",
        "research engineer",
        "robotics engineer",
        "simulation engineer",
    }

    REJECT_TITLES = {
        "sales",
        "sales closer",
        "marketing",
        "designer",
        "graphic designer",
        "interface designer",
        "ui designer",
        "ux designer",
        "crm",
        "crm manager",
        "lifecycle manager",
        "customer success",
        "customer support",
        "customer service",
        "recruiter",
        "account executive",
        "account manager",
        "business development",
        "finance",
        "hr",
        "human resources",
        "operations manager",
        "virtual assistant",
        "cashier",
        "warehouse",
        "driver",
        "delivery",
        "cook",
        "chef",
        "bartender",
        "nurse",
        "receptionist",
    }

    TECH_SKILLS = {
        "python",
        "java",
        "c++",
        "c#",
        "javascript",
        "typescript",
        "react",
        "node",
        "django",
        "flask",
        "fastapi",
        "spring",
        "sql",
        "postgresql",
        "mysql",
        "mongodb",
        "redis",
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "gcp",
        "tensorflow",
        "pytorch",
        "langchain",
        "llamaindex",
        "rag",
        "llm",
        "huggingface",
        "openai",
        "rest api",
        "git",
        "github",
    }

    AI_KEYWORDS = {
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "generative ai",
        "computer vision",
        "natural language processing",
        "nlp",
        "llm",
        "rag",
        "agentic ai",
    }

    EXPERIENCE_KEYWORDS = {
        "software development",
        "backend development",
        "api development",
        "distributed systems",
        "microservices",
        "ml pipeline",
        "production systems",
    }

    @staticmethod
    def _contains_phrase(text: str, phrase: str) -> bool:
        pattern = r"\b" + re.escape(phrase) + r"\b"
        return re.search(pattern, text) is not None

    @classmethod
    def filter_job(
        cls,
        title: str,
        description: str,
    ) -> FilterResult:

        title = (title or "").lower()
        description = (description or "").lower()

        text = f"{title} {description}"

        # Reject immediately
        for keyword in cls.REJECT_TITLES:
            if cls._contains_phrase(title, keyword):
                return FilterResult(
                    accepted=False,
                    confidence=1.0,
                    score=0,
                    reason=f"Rejected because title contains '{keyword}'.",
                )

        score = 0

        # Strong title match
        for keyword in cls.ALLOWED_TITLES:
            if cls._contains_phrase(title, keyword):
                score += 50
                break

        matched_skills = sum(
            1
            for skill in cls.TECH_SKILLS
            if skill in text
        )

        score += matched_skills * 2

        matched_ai = sum(
            1
            for keyword in cls.AI_KEYWORDS
            if keyword in text
        )

        score += matched_ai * 5

        matched_exp = sum(
            1
            for keyword in cls.EXPERIENCE_KEYWORDS
            if keyword in text
        )

        score += matched_exp * 10

        if score >= 70:
            return FilterResult(
                accepted=True,
                confidence=0.95,
                score=score,
                reason="Excellent AI/Software Engineering match.",
            )

        if score >= 50:
            return FilterResult(
                accepted=True,
                confidence=0.75,
                score=score,
                reason="Relevant software engineering job.",
            )

        return FilterResult(
            accepted=False,
            confidence=0.25,
            score=score,
            reason="Low relevance for AI/Software Engineering.",
        )