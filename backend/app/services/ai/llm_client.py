import json
import logging

import anthropic

from backend.app.core.config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Thin wrapper around the Anthropic Claude Messages API.

    Every AI-generation service (resume tailoring, cover letters,
    recommendation copy, ATS score, etc.) should go through this class instead
    of calling the SDK directly, so the model name / retries / error
    handling only live in one place.
    """

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.model = model or settings.ANTHROPIC_MODEL
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        # The SDK auto-retries 429/5xx and connection errors with exponential
        # backoff; bump the default (2) for resilience against transient
        # rate limits during the daily discovery pipeline.
        self.client = anthropic.Anthropic(
            api_key=self.api_key or None,
            max_retries=4,
        )

    def generate_text(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.0,
    ) -> str:
        """Return a plain-text completion.

        ``temperature`` is accepted for backwards compatibility but not sent to
        the API — current Claude models (Opus 4.8 / Sonnet 5) reject sampling
        parameters. Steer behaviour via the prompt instead.
        """

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )
        except anthropic.APIStatusError as e:
            logger.warning("LLM API error: %s - %s", e.status_code, e.message)
            raise
        except anthropic.APIConnectionError as e:
            logger.warning("LLM connection error: %s", e)
            raise
        except Exception:
            logger.exception("LLM generate_text failed (non-retryable)")
            raise

        if response.stop_reason == "refusal":
            raise ValueError("LLM declined the request (refusal)")

        text_content = "".join(
            block.text for block in response.content if block.type == "text"
        )

        if not text_content.strip():
            raise ValueError(f"LLM returned no text content: {response.stop_reason}")

        return text_content.strip()

    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.0,
    ) -> dict:
        """
        Return a parsed JSON object. Assumes the system prompt instructs
        the model to respond with JSON only (no prose, no code fences).
        """

        # Append JSON instruction for the model.
        system_prompt += "\n\nIMPORTANT: Return ONLY valid JSON. Do not use markdown blocks like ```json."

        raw = self.generate_text(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        cleaned = raw.strip()

        # Remove markdown fences if the model still generates them
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        cleaned = cleaned.strip()

        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

        # Find first '{' or '[' and last '}' or ']'
        start_obj = cleaned.find('{')
        start_arr = cleaned.find('[')
        start = start_obj if start_arr == -1 else (start_arr if start_obj == -1 else min(start_obj, start_arr))

        end_obj = cleaned.rfind('}')
        end_arr = cleaned.rfind(']')
        end = end_obj if end_arr == -1 else (end_arr if end_obj == -1 else max(end_obj, end_arr))

        if start != -1 and end != -1 and end > start:
            cleaned = cleaned[start:end+1]

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            logger.error("LLM did not return valid JSON: %s", raw[:500])
            raise
