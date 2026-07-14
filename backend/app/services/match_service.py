from backend.app.repositories.parsed_resume_repository import ParsedResumeRepository
from backend.app.repositories.parsed_job_repository import ParsedJobRepository
from backend.app.schemas.match import MatchResponse


class MatchService:

    def __init__(
        self,
        parsed_resume_repository: ParsedResumeRepository,
        parsed_job_repository: ParsedJobRepository,
    ):
        self.parsed_resume_repository = parsed_resume_repository
        self.parsed_job_repository = parsed_job_repository


    def normalize_skills(
        self,
        skills,
    ) -> set[str]:

        normalized = set()

        if isinstance(skills, dict):

            for category_skills in skills.values():

                if isinstance(category_skills, list):

                    for skill in category_skills:
                        normalized.add(
                            skill.strip().lower()
                        )

        elif isinstance(skills, list):

            for skill in skills:
                normalized.add(
                    skill.strip().lower()
                )

        return normalized


    def match_resume_to_job(
        self,
        resume_id: int,
        job_id: int,
    ) -> MatchResponse | None:

        parsed_resume = self.parsed_resume_repository.get_by_resume_id(
            resume_id
        )

        parsed_job = self.parsed_job_repository.get_by_job_id(
            job_id
        )


        if parsed_resume is None or parsed_job is None:
            return None


        resume_skills = self.normalize_skills(
            parsed_resume.skills
        )

        job_skills = self.normalize_skills(
            parsed_job.skills
        )


        matched_skills = sorted(
            resume_skills & job_skills
        )


        missing_skills = sorted(
            job_skills - resume_skills
        )


        if len(job_skills) == 0:
            match_score = 0

        else:
            match_score = round(
                (
                    len(matched_skills)
                    /
                    len(job_skills)
                )
                * 100,
                2,
            )


        recommendations = [
            f"Consider adding experience with {skill.title()}."
            for skill in missing_skills
        ]


        return MatchResponse(
            resume_id=resume_id,
            job_id=job_id,
            match_score=match_score,
            matched_skills=[
                skill.title()
                for skill in matched_skills
            ],
            missing_skills=[
                skill.title()
                for skill in missing_skills
            ],
            recommendations=recommendations,
        )