from dataclasses import dataclass
from urllib.parse import urlparse

# These platforms are never auto-applied to. We only ever hand back the
# link (and, where the platform exposes one, an "Easy Apply"-style link)
# so the person can review and submit the application themselves.
MANUAL_ONLY_DOMAINS = {
    "linkedin.com",
    "www.linkedin.com",
    "indeed.com",
    "www.indeed.com",
    "joinhandshake.com",
    "app.joinhandshake.com",
    "handshake.com",
}

# Job-board/ATS platforms whose public application pages are stable enough
# that a direct link can be handed to an automated-submission flow.
DIRECT_APPLY_DOMAINS_HINTS = (
    "greenhouse.io",
    "lever.co",
    "ashbyhq.com",
    "myworkdayjobs.com",
    "smartrecruiters.com",
    "workable.com",
)


@dataclass
class ApplyClassification:
    apply_url: str
    domain: str
    auto_apply_eligible: bool
    reason: str


class ApplyClassifierService:
    """
    Decides, per job, whether the "Apply" click can attempt a direct
    automated submission or whether it must only ever hand the person
    a link to apply manually.
    """

    @staticmethod
    def classify(apply_url: str | None) -> ApplyClassification:

        if not apply_url:
            return ApplyClassification(
                apply_url="",
                domain="",
                auto_apply_eligible=False,
                reason="No apply URL available.",
            )

        domain = (urlparse(apply_url).netloc or "").lower()

        if domain in MANUAL_ONLY_DOMAINS:
            return ApplyClassification(
                apply_url=apply_url,
                domain=domain,
                auto_apply_eligible=False,
                reason=(
                    "LinkedIn, Indeed, and Handshake are always manual-apply "
                    "by design; only the link is provided."
                ),
            )

        if any(hint in domain for hint in DIRECT_APPLY_DOMAINS_HINTS):
            return ApplyClassification(
                apply_url=apply_url,
                domain=domain,
                auto_apply_eligible=True,
                reason=f"Direct ATS link on {domain}; eligible for fast apply.",
            )

        return ApplyClassification(
            apply_url=apply_url,
            domain=domain,
            auto_apply_eligible=False,
            reason=(
                f"Unrecognized domain '{domain}'; defaulting to manual apply "
                "until this ATS is explicitly supported."
            ),
        )
