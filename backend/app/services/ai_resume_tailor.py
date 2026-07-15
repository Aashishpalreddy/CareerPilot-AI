import json

import anthropic

from backend.app.core.config import settings
from backend.app.schemas.resume_tailor import (
    ResumeTailorResponse,
    TailoredBullet,
)


class AIResumeTailor:

    def __init__(self):

        print("========== AI RESUME TAILOR ==========")
        print("API Key Loaded:", bool(settings.ANTHROPIC_API_KEY))
        print(
            "API Key Prefix:",
            settings.ANTHROPIC_API_KEY[:10]
            if settings.ANTHROPIC_API_KEY
            else "EMPTY",
        )

        self.client = anthropic.Anthropic(
            api_key=settings.ANTHROPIC_API_KEY,
        )

    def tailor(
        self,
        parsed_resume: dict,
        parsed_job: dict,
    ) -> ResumeTailorResponse:

        prompt = f"""
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
- Do NOT wrap the JSON inside markdown.

Resume

{json.dumps(parsed_resume, indent=2)}

Job

{json.dumps(parsed_job, indent=2)}

Return JSON exactly like this:

{{
  "tailored_summary":"",
  "tailored_experience":[],
  "tailored_projects":[],
  "ats_keywords":[],
  "tailored_bullets":[],
  "keywords_added":[],
  "keywords_missing":[]
}}
"""

        response = self.client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=8000,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        result = response.content[0].text.strip()

        if result.startswith("```json"):
            result = result[7:]

        if result.startswith("```"):
            result = result[3:]

        if result.endswith("```"):
            result = result[:-3]

        result = result.strip()

        print("\n========== CLAUDE RAW RESPONSE ==========\n")
        print(result)
        print("\n========== END RESPONSE ==========\n")

        data = json.loads(result)

        tailored_bullets = []

        for bullet in data.get(
            "tailored_bullets",
            [],
        ):

            if isinstance(
                bullet,
                dict,
            ):
                tailored_bullets.append(
                    TailoredBullet(
                        section=bullet.get(
                            "section",
                            "Experience",
                        ),
                        bullet=bullet.get(
                            "bullet",
                            "",
                        ),
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
            tailored_summary=data.get(
                "tailored_summary",
                "",
            ),
            tailored_experience=data.get(
                "tailored_experience",
                [],
            ),
            tailored_projects=data.get(
                "tailored_projects",
                [],
            ),
            ats_keywords=data.get(
                "ats_keywords",
                [],
            ),
            tailored_bullets=tailored_bullets,
            keywords_added=data.get(
                "keywords_added",
                [],
            ),
            keywords_missing=data.get(
                "keywords_missing",
                [],
            ),
        )