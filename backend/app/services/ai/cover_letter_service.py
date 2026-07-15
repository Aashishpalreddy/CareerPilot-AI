import logging

from backend.app.repositories.parsed_job_repository import (
    ParsedJobRepository,
)
from backend.app.repositories.parsed_resume_repository import (
    ParsedResumeRepository,
)
from backend.app.schemas.cover_letter import (
    CoverLetterGenerateResponse,
)
from backend.app.services.ai.llm_client import LLMClient

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You write short, specific cover letters (250-350 words).

Rules:
- Only reference experience that actually appears in the candidate's resume.
- Open with why this role/company specifically.
- Reference 2-3 concrete pieces of the candidate's real experience.
- Do not invent experience.
- No clichés.
- Professional tone.
- Return JSON only.

{
    "cover_letter_text":"..."
}
"""


class CoverLetterService:

    def __init__(
        self,
        parsed_resume_repository: ParsedResumeRepository,
        parsed_job_repository: ParsedJobRepository,
        llm_client: LLMClient | None = None,
    ):
        self.parsed_resume_repository = parsed_resume_repository
        self.parsed_job_repository = parsed_job_repository
        self.llm_client = llm_client or LLMClient()

    def generate_cover_letter(
        self,
        resume_id: int,
        job_id: int,
    ) -> CoverLetterGenerateResponse | None:

        parsed_resume = self.parsed_resume_repository.get_by_resume_id(
            resume_id
        )

        parsed_job = self.parsed_job_repository.get_by_job_id(
            job_id
        )

        if parsed_resume is None or parsed_job is None:
            return None

        user_prompt = (
            f"CANDIDATE RESUME:\n\n"
            f"{parsed_resume.raw_text}\n\n"
            f"TARGET JOB\n\n"
            f"Title: {parsed_job.title or 'Unknown'}\n"
            f"Company: {parsed_job.company or 'Unknown'}\n\n"
            f"{parsed_job.raw_text}\n\n"
            f"Generate the cover letter."
        )

        try:

            result = self.llm_client.generate_json(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=user_prompt,
                max_tokens=1200,
            )

            return CoverLetterGenerateResponse(
                cover_letter_text=result.get(
                    "cover_letter_text",
                    "",
                )
            )

        except Exception:

            logger.exception(
                "Failed generating cover letter."
            )

            return None