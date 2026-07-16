import json
import logging
import httpx

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from backend.app.core.config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Thin wrapper around the Google Gemini REST API.

    Every AI-generation service (resume tailoring, cover letters,
    recommendation copy, ATS score, etc.) should go through this class instead
    of calling the SDK directly, so the model name / retries / error
    handling only live in one place.
    """

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.model = model or settings.GEMINI_MODEL
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        retry=retry_if_exception_type(
            (httpx.RequestError, httpx.HTTPStatusError, ValueError)
        ),
        reraise=True,
    )
    def generate_text(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.0,
    ) -> str:
        """Return a plain-text completion with automatic retry on transient errors."""

        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": self.api_key,
        }

        payload = {
            "systemInstruction": {
                "parts": [{"text": system_prompt}]
            },
            "contents": [
                {
                    "parts": [{"text": user_prompt}]
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            }
        }

        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(self.base_url, headers=headers, json=payload)
                response.raise_for_status()
                
                data = response.json()
                
                # Extract text from Gemini response structure
                if "candidates" not in data or not data["candidates"]:
                    raise ValueError(f"No candidates returned by Gemini: {data}")
                
                candidate = data["candidates"][0]
                if "content" not in candidate or "parts" not in candidate["content"]:
                    raise ValueError(f"Unexpected candidate structure: {candidate}")
                
                parts = candidate["content"]["parts"]
                text_content = "".join(part.get("text", "") for part in parts)
                
                return text_content.strip()

        except httpx.HTTPStatusError as e:
            logger.warning(f"LLM API Error: {e.response.status_code} - {e.response.text}")
            raise
        except (httpx.RequestError, ValueError) as e:
            logger.warning(f"LLM transient error — will retry: {str(e)}")
            raise
        except Exception:
            logger.exception("LLM generate_text failed (non-retryable)")
            raise

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

        # Append JSON instruction for Gemini
        system_prompt += "\n\nIMPORTANT: Return ONLY valid JSON. Do not use markdown blocks like ```json."

        raw = self.generate_text(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        cleaned = raw.strip()
        
        # Remove markdown fences if model still generates them
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
