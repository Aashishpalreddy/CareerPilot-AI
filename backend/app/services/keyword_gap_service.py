from backend.app.models.parsed_job import ParsedJob
from backend.app.models.parsed_resume import ParsedResume
from backend.app.schemas.keyword_gap import (
    KeywordGapResponse,
    MatchResult,
)


class KeywordGapService:

    SKILL_WEIGHT = 0.40
    TECHNOLOGY_WEIGHT = 0.20
    CERTIFICATION_WEIGHT = 0.10
    EXPERIENCE_WEIGHT = 0.20
    EDUCATION_WEIGHT = 0.10

    @staticmethod
    def _normalize(values):

        if not values:
            return set()

        return {
            str(value).strip().lower()
            for value in values
            if value and str(value).strip()
        }

    @classmethod
    def _compare(cls, resume_items, job_items):

        resume = cls._normalize(resume_items)
        job = cls._normalize(job_items)

        matched = sorted(resume & job)
        missing = sorted(job - resume)

        return matched, missing

    @staticmethod
    def _score(matched, required):

        if required == 0:
            return 100.0

        return round((matched / required) * 100, 2)

    @staticmethod
    def _experience(parsed_resume, parsed_job):

        if parsed_resume.years_experience is None:
            return False

        return parsed_resume.years_experience > 0

    @staticmethod
    def _education(parsed_resume, parsed_job):

        return bool(parsed_resume.education)

    @staticmethod
    def _recommendations(
        skill_missing,
        technology_missing,
        certification_missing,
    ):

        recommendations = []

        if skill_missing:
            recommendations.append(
                "Add or highlight these required skills: "
                + ", ".join(skill_missing)
            )

        if technology_missing:
            recommendations.append(
                "Highlight experience with: "
                + ", ".join(technology_missing)
            )

        if certification_missing:
            recommendations.append(
                "Include certifications if applicable: "
                + ", ".join(certification_missing)
            )

        if not recommendations:
            recommendations.append(
                "Resume is well aligned with this job."
            )

        return recommendations

    def analyze(
        self,
        parsed_resume: ParsedResume,
        parsed_job: ParsedJob,
    ) -> KeywordGapResponse:

        matched_skills, missing_skills = self._compare(
            parsed_resume.skills,
            parsed_job.skills,
        )

        matched_technologies, missing_technologies = self._compare(
            parsed_resume.technologies,
            parsed_job.technologies,
        )

        matched_certifications, missing_certifications = self._compare(
            parsed_resume.certifications,
            parsed_job.certifications,
        )

        skill_score = self._score(
            len(matched_skills),
            len(self._normalize(parsed_job.skills)),
        )

        technology_score = self._score(
            len(matched_technologies),
            len(self._normalize(parsed_job.technologies)),
        )

        certification_score = self._score(
            len(matched_certifications),
            len(self._normalize(parsed_job.certifications)),
        )

        experience_match = self._experience(
            parsed_resume,
            parsed_job,
        )

        education_match = self._education(
            parsed_resume,
            parsed_job,
        )

        experience_score = 100 if experience_match else 0
        education_score = 100 if education_match else 0

        overall_score = (
            skill_score * self.SKILL_WEIGHT
            + technology_score * self.TECHNOLOGY_WEIGHT
            + certification_score * self.CERTIFICATION_WEIGHT
            + experience_score * self.EXPERIENCE_WEIGHT
            + education_score * self.EDUCATION_WEIGHT
        )

        recommendations = self._recommendations(
            missing_skills,
            missing_technologies,
            missing_certifications,
        )

        return KeywordGapResponse(
            overall_score=round(overall_score, 2),
            skills=MatchResult(
                matched=matched_skills,
                missing=missing_skills,
                score=skill_score,
            ),
            technologies=MatchResult(
                matched=matched_technologies,
                missing=missing_technologies,
                score=technology_score,
            ),
            certifications=MatchResult(
                matched=matched_certifications,
                missing=missing_certifications,
                score=certification_score,
            ),
            experience_match=experience_match,
            education_match=education_match,
            recommendations=recommendations,
        )