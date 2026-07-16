import json
import logging

from backend.app.schemas.resume_tailor import (
    ResumeTailorResponse,
    TailoredBullet,
)
from backend.app.services.ai.llm_client import LLMClient

logger = logging.getLogger(__name__)


class AIResumeTailor:

    def __init__(self):
        self.client = LLMClient()

    def tailor(
        self,
        parsed_resume: dict,
        parsed_job: dict,
        ats_feedback: dict | None = None,
    ) -> ResumeTailorResponse:

        system_prompt = """
You are an expert ATS Resume Writer.

Your task is to tailor the candidate's resume for the target job.

Rules:

- Never invent experience.
- Never invent projects.
- Never invent certifications.
- Never invent education.
- Never invent skills.
- Never rename companies.
- Never rename projects.
- Improve wording only.
- Add ATS keywords naturally.
- Rewrite the professional summary.
- Improve existing experience bullets.
- Improve existing project bullets.
- Return ONLY valid JSON.

Return JSON exactly like this:
{
  "tailored_summary":"",
  "tailored_experience":[],
  "tailored_projects":[],
  "ats_keywords":[],
  "tailored_bullets":[],
  "keywords_added":[],
  "keywords_missing":[]
}
"""

        user_prompt = f"""
Resume:
{json.dumps(parsed_resume, indent=2)}

Job:
{json.dumps(parsed_job, indent=2)}

{"Previous ATS Feedback to FIX:\n" + json.dumps(ats_feedback, indent=2) + "\n\nYou MUST improve the resume to resolve these weaknesses and implement the suggestions." if ats_feedback else ""}
"""
        
        try:
            data = self.client.generate_json(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_tokens=8000,
            )

            tailored_bullets = []
            for bullet in data.get("tailored_bullets", []):
                if isinstance(bullet, dict):
                    tailored_bullets.append(
                        TailoredBullet(
                            section=bullet.get("section", "Experience"),
                            bullet=bullet.get("bullet", ""),
                        )
                    )
                else:
                    tailored_bullets.append(
                        TailoredBullet(
                            section="Experience",
                            bullet=str(bullet),
                        )
                    )

            return ResumeTailorResponse(
                resume_id=0,
                job_id=0,
                original_match_score=0,
                improved_match_score=0,
                tailored_summary=data.get("tailored_summary", ""),
                tailored_experience=data.get("tailored_experience", []),
                tailored_projects=data.get("tailored_projects", []),
                ats_keywords=data.get("ats_keywords", []),
                tailored_bullets=tailored_bullets,
                keywords_added=data.get("keywords_added", []),
                keywords_missing=data.get("keywords_missing", []),
            )
        except Exception as e:
            logger.exception("AI resume tailoring failed.")
            raise RuntimeError(f"Failed to tailor resume: {e}") from e