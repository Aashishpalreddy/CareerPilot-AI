import asyncio
import logging
from typing import Any

import httpx

from backend.app.integrations.jobs.base import JobProvider
from backend.app.integrations.jobs.companies import GREENHOUSE_COMPANIES

logger = logging.getLogger(__name__)

# Limit concurrent requests to avoid hammering the API
MAX_CONCURRENT = 8


class GreenhouseProvider(JobProvider):

    BASE_URL = "https://boards-api.greenhouse.io/v1/boards"

    @property
    def provider_name(self) -> str:
        return "Greenhouse"

    async def _fetch_company_jobs(
        self,
        client: httpx.AsyncClient,
        company: str,
        keyword_set: set[str],
        location: str | None,
        remote_only: bool,
        semaphore: asyncio.Semaphore,
    ) -> list[dict[str, Any]]:
        """Fetch and filter jobs for a single company."""

        async with semaphore:
            try:
                response = await client.get(
                    f"{self.BASE_URL}/{company}/jobs",
                    params={"content": "true"},
                )

                if response.status_code != 200:
                    return []

                data = response.json()
                jobs = data.get("jobs", [])
                logger.debug("%s: %d jobs found", company, len(jobs))

                results: list[dict[str, Any]] = []

                for job in jobs:
                    title = job.get("title", "")
                    description = job.get("content") or ""
                    location_name = (
                        job.get("location", {}).get("name")
                        if job.get("location")
                        else ""
                    )

                    search_text = (title + " " + description).lower()

                    if keyword_set and not any(
                        keyword in search_text for keyword in keyword_set
                    ):
                        continue

                    if remote_only:
                        remote_keywords = [
                            "remote", "work from home", "anywhere", "distributed",
                        ]
                        if not any(
                            word in location_name.lower()
                            for word in remote_keywords
                        ):
                            continue

                    if location and location.lower() not in location_name.lower():
                        continue

                    results.append({
                        "title": title,
                        "company": company.replace("-", " ").title(),
                        "location": location_name,
                        "description": description,
                        "job_url": job.get("absolute_url"),
                        "source": self.provider_name,
                    })

                return results

            except Exception:
                logger.exception("Greenhouse error (%s)", company)
                return []

    async def search_jobs(
        self,
        keywords: list[str],
        location: str | None = None,
        remote_only: bool = False,
        max_results: int = 50,
    ) -> list[dict[str, Any]]:

        keyword_set = {kw.lower().strip() for kw in keywords}
        semaphore = asyncio.Semaphore(MAX_CONCURRENT)

        async with httpx.AsyncClient(timeout=30) as client:
            tasks = [
                self._fetch_company_jobs(
                    client, company, keyword_set, location, remote_only, semaphore,
                )
                for company in GREENHOUSE_COMPANIES
            ]

            all_results = await asyncio.gather(*tasks)

        # Flatten and cap
        normalized: list[dict[str, Any]] = []
        for company_jobs in all_results:
            for job in company_jobs:
                normalized.append(job)
                if len(normalized) >= max_results:
                    break
            if len(normalized) >= max_results:
                break

        logger.info("Greenhouse returned %d matching jobs", len(normalized))
        return normalized