import logging

from backend.app.schemas.job_parser import JobParserResponse
from backend.app.prompts.job_parser_prompt import JOB_PARSER_PROMPT
from backend.app.services.ai.llm_client import LLMClient

logger = logging.getLogger(__name__)


class AIJobParser:
    """
    Uses Google Gemini via LLMClient to convert an unstructured job description
    into a structured JobParserResponse.
    """

    def __init__(self):
        self.client = LLMClient()

    def parse(
        self,
        job_description: str
    ) -> JobParserResponse:
        
        # The prompt originally has the system instructions and the job description combined.
        # Let's separate it if possible, or just pass it as system prompt.
        
        system_prompt = "You are an expert AI recruiter that extracts structured information from job descriptions."
        user_prompt = JOB_PARSER_PROMPT.format(job_description=job_description)

        try:
            parsed_json = self.client.generate_json(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_tokens=4096,
            )

            return JobParserResponse.model_validate(
                parsed_json
            )

        except Exception as e:
            logger.exception(
                "AI job parsing failed."
            )
            raise RuntimeError(
                f"Failed to parse job description using AI: {str(e)}"
            ) from e