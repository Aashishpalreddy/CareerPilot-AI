from dataclasses import dataclass
import logging

from backend.app.services.ai.llm_client import LLMClient

logger = logging.getLogger(__name__)

@dataclass
class FilterResult:
    accepted: bool
    confidence: float
    score: int
    reason: str


class JobFilterService:

    @classmethod
    def filter_job(
        cls,
        title: str,
        description: str,
    ) -> FilterResult:
        title = (title or "").strip()
        description = (description or "").strip()
        
        if not title and not description:
            return FilterResult(False, 1.0, 0, "No title or description provided.")

        system_prompt = """
You are an expert Job Filter AI for a software engineering/AI career platform.

Your task is to evaluate the following job title and description and determine if it is highly relevant for a software engineer, data scientist, or AI/ML engineer.
Reject jobs that are not related to software engineering or AI (e.g., sales, marketing, generic IT support, warehouse, etc.).

Return JSON in this exact format:
{
    "accepted": true/false,
    "confidence": 0.0 to 1.0,
    "score": 0 to 100,
    "reason": "A short, one sentence explanation of why it was accepted or rejected."
}
"""
        
        user_prompt = f"""
Job Title: {title}
Job Description: {description[:3000]}
"""

        try:
            client = LLMClient()
            parsed = client.generate_json(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_tokens=1024,
            )
            
            return FilterResult(
                accepted=bool(parsed.get("accepted", False)),
                confidence=float(parsed.get("confidence", 0.0)),
                score=int(parsed.get("score", 0)),
                reason=str(parsed.get("reason", "No reason provided.")),
            )
        except Exception as e:
            logger.exception(f"Failed to filter job with AI API: {e}")
            # Fail closed: if the AI filter call errors (timeout, rate limit),
            # reject rather than fall back to broad keyword matching that lets
            # through irrelevant jobs (e.g. "data" matching "Data Entry Clerk").
            return FilterResult(False, 0.0, 0, "Rejected: AI filter unavailable.")