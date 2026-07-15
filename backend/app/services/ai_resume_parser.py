import json
import logging

from anthropic import Anthropic

from backend.app.core.config import settings
from backend.app.schemas.resume_profile import ResumeProfile

logger = logging.getLogger(__name__)


class AIResumeParser:
    """
    Uses Anthropic Claude to convert an unstructured resume into a
    structured ResumeProfile.
    """

    def __init__(self):
        self.client = Anthropic(
            api_key=settings.ANTHROPIC_API_KEY
        )

    @staticmethod
    def _extract_json(text: str) -> dict:
        """
        Claude may wrap JSON in markdown or include explanatory text.
        This method extracts the JSON object safely.
        """

        text = text.strip()

        # Remove markdown fences
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        start = text.find("{")
        end = text.rfind("}") + 1

        if start == -1 or end == 0:
            raise ValueError("No JSON object found in Claude response.")

        json_text = text[start:end]

        return json.loads(json_text)

    def parse(self, resume_text: str) -> ResumeProfile:
        prompt = f"""
You are an expert ATS Resume Parser.

Your task is to extract structured information from the resume.

IMPORTANT RULES:

- Return ONLY valid JSON.
- Do NOT include markdown.
- Do NOT include explanations.
- Do NOT hallucinate information.
- If information is unavailable, use:
  - "" for strings
  - [] for arrays
  - 0 for numeric values

Return JSON in this exact format:

{{
    "summary": "",
    "skills": [],
    "experience": [],
    "education": [],
    "projects": [],
    "certifications": [],
    "technologies": [],
    "languages": [],
    "achievements": [],
    "years_experience": 0
}}

Resume:

{resume_text}
"""

        try:
            response = self.client.messages.create(
                model=settings.ANTHROPIC_MODEL,
                max_tokens=4096,
                temperature=0,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            response_text = response.content[0].text

            parsed_json = self._extract_json(response_text)

            return ResumeProfile.model_validate(parsed_json)

        except Exception as e:
            logger.exception("AI resume parsing failed.")
            raise RuntimeError(
                f"Failed to parse resume using AI: {str(e)}"
            ) from e