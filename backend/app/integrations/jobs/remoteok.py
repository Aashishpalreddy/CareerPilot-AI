from typing import Any

import httpx

from backend.app.integrations.jobs.base import JobProvider


class RemoteOKProvider(JobProvider):

    @property
    def provider_name(self) -> str:
        return "RemoteOK"

    async def search_jobs(
        self,
        keywords: list[str],
        location: str | None = None,
        remote_only: bool = False,
        max_results: int = 50,
    ) -> list[dict[str, Any]]:

        url = "https://remoteok.com/api"

        headers = {
            "User-Agent": "CareerPilot-AI",
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                url,
                headers=headers,
            )

            response.raise_for_status()

        jobs = response.json()

        # Remove API metadata
        if (
            jobs
            and isinstance(jobs[0], dict)
            and jobs[0].get("legal")
        ):
            jobs = jobs[1:]

        normalized_jobs = []

        keyword_set = {
            keyword.lower().strip()
            for keyword in keywords
        }

        print("\n" + "=" * 80)
        print(f"RemoteOK returned {len(jobs)} jobs")
        print("=" * 80)

        for job in jobs:

            title = (
                job.get("position")
                or job.get("title")
                or job.get("role")
                or ""
            )

            description = (
                job.get("description")
                or ""
            )

            tags = [
                tag.lower()
                for tag in job.get("tags", [])
            ]

            # Search only title + tags
            search_text = (
                title.lower()
                + " "
                + " ".join(tags)
            )

            if keyword_set:

                if not any(
                    keyword in search_text
                    for keyword in keyword_set
                ):
                    continue

            print(f"Matched: {title}")

            normalized_jobs.append(
                {
                    "title": title,
                    "company": job.get("company"),
                    "location": job.get("location") or "Remote",
                    "description": description,
                    "job_url": (
                        job.get("apply_url")
                        or job.get("url")
                    ),
                    "source": self.provider_name,
                }
            )

            if len(normalized_jobs) >= max_results:
                break

        print(f"Filtered Jobs: {len(normalized_jobs)}")

        return normalized_jobs