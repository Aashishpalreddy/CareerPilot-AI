from typing import Any

import httpx

from backend.app.integrations.jobs.base import JobProvider


class RemotiveProvider(JobProvider):
    """
    Free, keyless remote-jobs API (https://remotive.com/api-documentation).
    Complements RemoteOK with a separate listing pool so a single flaky/rate
    limited provider doesn't leave discovery with almost no results.
    """

    BASE_URL = "https://remotive.com/api/remote-jobs"

    @property
    def provider_name(self) -> str:
        return "Remotive"

    async def search_jobs(
        self,
        keywords: list[str],
        location: str | None = None,
        remote_only: bool = False,
        max_results: int = 50,
    ) -> list[dict[str, Any]]:

        headers = {"User-Agent": "CareerPilot-AI"}

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                self.BASE_URL,
                params={"category": "software-dev"},
                headers=headers,
            )
            response.raise_for_status()

        jobs = response.json().get("jobs", [])

        keyword_set = {keyword.lower().strip() for keyword in keywords}

        normalized_jobs = []

        for job in jobs:
            title = job.get("title") or ""
            description = job.get("description") or ""

            search_text = (title + " " + description).lower()

            if keyword_set and not any(
                keyword in search_text for keyword in keyword_set
            ):
                continue

            candidate_location = job.get("candidate_required_location") or "Remote"

            if location and location.lower() not in candidate_location.lower():
                continue

            normalized_jobs.append(
                {
                    "title": title,
                    "company": job.get("company_name"),
                    "location": candidate_location,
                    "description": description,
                    "job_url": job.get("url"),
                    "source": self.provider_name,
                }
            )

            if len(normalized_jobs) >= max_results:
                break

        return normalized_jobs
