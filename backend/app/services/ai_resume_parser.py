import logging

from backend.app.schemas.resume_profile import ResumeProfile
from backend.app.services.ai.llm_client import LLMClient

logger = logging.getLogger(__name__)


class AIResumeParser:
    """
    Uses Claude via LLMClient to convert an unstructured resume into a
    structured ResumeProfile.
    """

    def __init__(self):
        self.client = LLMClient()

    def parse(self, resume_text: str) -> ResumeProfile:
        system_prompt = """
You are an expert ATS Resume Parser.

Your task is to extract structured information from the resume.

IMPORTANT RULES:
- Do NOT hallucinate information.
- If information is unavailable, use:
  - "" for strings
  - [] for arrays
  - 0 for numeric values
- Each "description" must be a single string (join bullet points with newlines).
- Each certification must be an object, not a plain string.

Return JSON in this exact format (respect the field shapes):
{
    "summary": "",
    "skills": ["string"],
    "experience": [
        {"company": "", "title": "", "location": "", "start_date": "", "end_date": "", "description": ""}
    ],
    "education": [
        {"institution": "", "degree": "", "field_of_study": "", "start_date": "", "end_date": ""}
    ],
    "projects": [
        {"name": "", "description": "", "technologies": ["string"]}
    ],
    "certifications": [
        {"name": "", "issuer": "", "issue_date": ""}
    ],
    "technologies": ["string"],
    "languages": ["string"],
    "achievements": ["string"],
    "years_experience": 0
}
"""
        
        user_prompt = f"""
Resume:

{resume_text}
"""

        try:
            parsed_json = self.client.generate_json(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_tokens=4096,
            )

            return ResumeProfile.model_validate(parsed_json)

        except Exception as e:
            logger.exception("AI resume parsing failed.")
            raise RuntimeError(
                f"Failed to parse resume using AI: {str(e)}"
            ) from e