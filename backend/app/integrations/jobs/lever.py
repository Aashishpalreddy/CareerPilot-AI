import asyncio
import logging
from typing import Any

import httpx

from backend.app.integrations.jobs.base import JobProvider
from backend.app.integrations.jobs.companies import LEVER_COMPANIES

logger = logging.getLogger(__name__)

# Limit concurrent requests to avoid hammering the API
MAX_CONCURRENT = 8


class LeverProvider(JobProvider):

    BASE_URL = "https://api.lever.co/v0/postings"

    @property
    def provider_name(self) -> str:
        return "Lever"

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
                    f"{self.BASE_URL}/{company}",
                    params={"mode": "json"},
                )

                if response.status_code != 200:
                    return []

                postings = response.json()
                if not isinstance(postings, list):
                    return []

                logger.debug("%s: %d jobs found", company, len(postings))

                results: list[dict[str, Any]] = []

                for posting in postings:
                    title = posting.get("text", "")
                    description = (
                        posting.get("descriptionPlain")
                        or posting.get("description")
                        or ""
                    )
                    categories = posting.get("categories") or {}
                    location_name = categories.get("location") or ""

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
                        "job_url": (
                            posting.get("hostedUrl")
                            or posting.get("applyUrl")
                        ),
                        "source": self.provider_name,
                    })

                return results

            except Exception:
                logger.exception("Lever error (%s)", company)
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
                for company in LEVER_COMPANIES
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

        logger.info("Lever returned %d matching jobs", len(normalized))
        return normalized
