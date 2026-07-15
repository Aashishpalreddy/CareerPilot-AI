from backend.app.models.parsed_job import ParsedJob
from backend.app.models.parsed_resume import ParsedResume

from backend.app.schemas.resume_match import ResumeMatchResponse
from backend.app.services.keyword_gap_service import KeywordGapService


class ResumeMatchService:

    def __init__(self):
        self.keyword_gap = KeywordGapService()

    @staticmethod
    def _fit_level(score: float) -> str:

        if score >= 90:
            return "Excellent Match"

        if score >= 75:
            return "Strong Match"

        if score >= 60:
            return "Good Match"

        if score >= 40:
            return "Average Match"

        return "Poor Match"

    @staticmethod
    def _recommendation(score: float) -> str:

        if score >= 90:
            return "Highly Recommended"

        if score >= 75:
            return "Recommended"

        if score >= 60:
            return "Recommended with Resume Tailoring"

        if score >= 40:
            return "Needs Significant Resume Improvements"

        return "Not Recommended"

    def match(
        self,
        parsed_resume: ParsedResume,
        parsed_job: ParsedJob,
    ) -> ResumeMatchResponse:

        gap = self.keyword_gap.analyze(
            parsed_resume,
            parsed_job,
        )

        return ResumeMatchResponse(
            overall_match=gap.overall_score,
            fit_level=self._fit_level(
                gap.overall_score
            ),
            recommendation=self._recommendation(
                gap.overall_score
            ),
            skills=gap.skills,
            technologies=gap.technologies,
            certifications=gap.certifications,
            experience_match=gap.experience_match,
            education_match=gap.education_match,
        )