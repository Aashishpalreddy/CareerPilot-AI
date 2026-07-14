from typing import Any

import httpx

from backend.app.integrations.jobs.base import JobProvider
from backend.app.integrations.jobs.companies import GREENHOUSE_COMPANIES


class GreenhouseProvider(JobProvider):

    BASE_URL = "https://boards-api.greenhouse.io/v1/boards"

    @property
    def provider_name(self) -> str:
        return "Greenhouse"

    async def search_jobs(
        self,
        keywords: list[str],
        location: str | None = None,
        remote_only: bool = False,
        max_results: int = 50,
    ) -> list[dict[str, Any]]:

        normalized_jobs: list[dict[str, Any]] = []

        keyword_set = {
            keyword.lower().strip()
            for keyword in keywords
        }

        async with httpx.AsyncClient(timeout=30) as client:

            for company in GREENHOUSE_COMPANIES:

                try:

                    response = await client.get(
                        f"{self.BASE_URL}/{company}/jobs",
                        params={"content": "true"},
                    )

                    if response.status_code != 200:
                        continue

                    data = response.json()

                    jobs = data.get("jobs", [])

                    print(f"{company}: {len(jobs)} jobs")

                    for job in jobs:

                        title = job.get("title", "")

                        description = job.get("content") or ""

                        location_name = (
                            job.get("location", {}).get("name")
                            if job.get("location")
                            else ""
                        )

                        search_text = (
                            title
                            + " "
                            + description
                        ).lower()

                        if keyword_set:

                            if not any(
                                keyword in search_text
                                for keyword in keyword_set
                            ):
                                continue

                        if remote_only:

                            remote_keywords = [
                                "remote",
                                "work from home",
                                "anywhere",
                                "distributed",
                            ]

                            if not any(
                                word in location_name.lower()
                                for word in remote_keywords
                            ):
                                continue

                        if location:

                            if location.lower() not in location_name.lower():
                                continue

                        normalized_jobs.append(
                            {
                                "title": title,
                                "company": company.replace("-", " ").title(),
                                "location": location_name,
                                "description": description,
                                "job_url": job.get("absolute_url"),
                                "source": self.provider_name,
                            }
                        )

                        if len(normalized_jobs) >= max_results:
                            return normalized_jobs

                except Exception as ex:
                    print(f"Greenhouse error ({company}): {ex}")
                    continue

        print(f"Greenhouse returned {len(normalized_jobs)} matching jobs")

        return normalized_jobs