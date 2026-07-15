import json
import logging

import anthropic

from backend.app.core.config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Thin wrapper around the Anthropic API.

    Every AI-generation service (resume tailoring, cover letters,
    recommendation copy, etc.) should go through this class instead
    of calling the SDK directly, so the model name / retries / error
    handling only live in one place.
    """

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.model = model or settings.ANTHROPIC_MODEL
        self._client = anthropic.Anthropic(
            api_key=api_key or settings.ANTHROPIC_API_KEY,
        )

    def generate_text(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 1500,
    ) -> str:
        """Return a plain-text completion."""

        try:
            response = self._client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt},
                ],
            )

            return "".join(
                block.text
                for block in response.content
                if block.type == "text"
            ).strip()

        except Exception:
            logger.exception("LLM generate_text failed")
            raise

    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 1500,
    ) -> dict:
        """
        Return a parsed JSON object. Assumes the system prompt instructs
        the model to respond with JSON only (no prose, no code fences).
        """

        raw = self.generate_text(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=max_tokens,
        )

        cleaned = raw.strip().strip("`")

        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            logger.error("LLM did not return valid JSON: %s", raw[:500])
            raise
