from typing import Any

import httpx

from backend.app.core.config import settings
from backend.app.integrations.jobs.base import JobProvider


class AdzunaProvider(JobProvider):
    """
    Official free Adzuna job-search API (developer.adzuna.com). Aggregates
    listings from thousands of job boards and company sites — the
    legitimate way to get broad, mainstream coverage without scraping
    LinkedIn/Indeed, both of which explicitly prohibit that in their ToS.

    Requires ADZUNA_APP_ID / ADZUNA_APP_KEY (free signup). If either is
    unset, search_jobs returns no results rather than erroring, same as
    any other provider failing — discovery just continues with whatever
    other providers return.
    """

    BASE_URL = "https://api.adzuna.com/v1/api/jobs/us/search/1"

    @property
    def provider_name(self) -> str:
        return "Adzuna"

    async def search_jobs(
        self,
        keywords: list[str],
        location: str | None = None,
        remote_only: bool = False,
        max_results: int = 50,
    ) -> list[dict[str, Any]]:

        if not settings.ADZUNA_APP_ID or not settings.ADZUNA_APP_KEY:
            return []

        params = {
            "app_id": settings.ADZUNA_APP_ID,
            "app_key": settings.ADZUNA_APP_KEY,
            "results_per_page": min(max_results, 50),
            "content-type": "application/json",
        }

        if keywords:
            # what_or = match ANY of the given terms, consistent with how
            # every other provider here treats a multi-keyword search.
            params["what_or"] = " ".join(keywords)

        if location:
            params["where"] = location

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()

        data = response.json()
        results = data.get("results", [])

        normalized_jobs = []

        for job in results:
            title = job.get("title") or ""
            description = job.get("description") or ""
            location_name = (job.get("location") or {}).get("display_name") or ""

            if remote_only:
                remote_keywords = ["remote", "work from home", "anywhere"]
                search_text = (title + " " + description + " " + location_name).lower()
                if not any(word in search_text for word in remote_keywords):
                    continue

            normalized_jobs.append(
                {
                    "title": title,
                    "company": (job.get("company") or {}).get("display_name"),
                    "location": location_name,
                    "description": description,
                    "job_url": job.get("redirect_url"),
                    "source": self.provider_name,
                }
            )

            if len(normalized_jobs) >= max_results:
                break

        return normalized_jobs
