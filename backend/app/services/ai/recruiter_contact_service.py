from urllib.parse import quote, urlencode


class RecruiterContactService:
    """
    Generates links to help the person find and connect with recruiters
    themselves. This deliberately does NOT scrape LinkedIn profiles or
    emails, and does NOT send connection requests automatically -
    LinkedIn's terms of service prohibit automating profile scraping and
    outreach, and doing so risks the account being restricted.

    Instead, it builds a pre-filled LinkedIn people-search URL the person
    can open with one click, plus a couple of search queries useful for
    finding a public recruiter email through legitimate means.
    """

    @staticmethod
    def build_linkedin_search_url(
        company: str,
        roles: list[str] | None = None,
    ) -> str:

        roles = roles or ["recruiter", "talent acquisition", "technical recruiter"]

        keywords = f"{company} " + " OR ".join(roles)

        params = {
            "keywords": keywords,
            "origin": "GLOBAL_SEARCH_HEADER",
        }

        return "https://www.linkedin.com/search/results/people/?" + urlencode(
            params, quote_via=quote
        )

    @staticmethod
    def build_company_people_search_url(company: str) -> str:
        return (
            "https://www.linkedin.com/search/results/people/?"
            + urlencode({"keywords": f"{company} recruiter"}, quote_via=quote)
        )

    @classmethod
    def build_contact_links(
        cls,
        company: str,
    ) -> dict[str, str]:

        return {
            "linkedin_recruiter_search": cls.build_linkedin_search_url(company),
            "linkedin_company_people_search": cls.build_company_people_search_url(
                company
            ),
        }
