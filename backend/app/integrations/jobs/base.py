from abc import ABC, abstractmethod
from typing import Any


class JobProvider(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Human-readable provider name.
        Example:
        RemoteOK
        Greenhouse
        Lever
        Wellfound
        """
        raise NotImplementedError

    @abstractmethod
    async def search_jobs(
        self,
        keywords: list[str],
        location: str | None = None,
        remote_only: bool = False,
        max_results: int = 50,
    ) -> list[dict[str, Any]]:
        """
        Search jobs from the provider and return
        normalized job dictionaries.

        Returned format:

        {
            "title": str,
            "company": str,
            "location": str,
            "description": str,
            "job_url": str,
            "source": str,
        }
        """
        raise NotImplementedError