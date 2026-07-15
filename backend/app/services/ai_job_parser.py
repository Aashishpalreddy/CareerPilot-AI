import json
import logging

from anthropic import Anthropic

from backend.app.core.config import settings
from backend.app.schemas.job_parser import JobParserResponse
from backend.app.prompts.job_parser_prompt import JOB_PARSER_PROMPT


logger = logging.getLogger(__name__)


class AIJobParser:
    """
    Uses Anthropic Claude to convert an unstructured job description
    into a structured JobParserResponse.
    """

    def __init__(self):

        self.client = Anthropic(
            api_key=settings.ANTHROPIC_API_KEY
        )


    @staticmethod
    def _extract_json(text: str) -> dict:
        """
        Extract JSON safely from Claude response.
        """

        text = text.strip()

        text = text.replace(
            "```json",
            ""
        )

        text = text.replace(
            "```",
            ""
        )

        text = text.strip()

        start = text.find("{")

        end = text.rfind("}") + 1


        if start == -1 or end == 0:

            raise ValueError(
                "No JSON object found in Claude response."
            )


        json_text = text[start:end]


        return json.loads(json_text)


    def parse(
        self,
        job_description: str
    ) -> JobParserResponse:

        prompt = JOB_PARSER_PROMPT.format(
            job_description=job_description
        )


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


            parsed_json = self._extract_json(
                response_text
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