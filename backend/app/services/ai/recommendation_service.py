from typing import Any

from backend.app.services.match_service import MatchService


class RecommendationService:
    """
    Ranks jobs based on resume-job match score.
    Uses existing MatchService.
    """

    def __init__(
        self,
        match_service: MatchService,
    ):
        self.match_service = match_service


    def recommend_jobs(
        self,
        resume_id: int,
        job_ids: list[int],
    ) -> list[dict[str, Any]]:

        recommendations = []

        for job_id in job_ids:

            match_result = self.match_service.match_resume_to_job(
                resume_id=resume_id,
                job_id=job_id,
            )

            if match_result is None:
                continue


            recommendation = {
                "job_id": job_id,
                "resume_id": resume_id,
                "match_score": match_result.match_score,
                "matched_skills": match_result.matched_skills,
                "missing_skills": match_result.missing_skills,
                "recommendations": match_result.recommendations,
            }


            if match_result.match_score >= 80:
                recommendation["decision"] = "Apply"
            
            elif match_result.match_score >= 60:
                recommendation["decision"] = "Review"

            else:
                recommendation["decision"] = "Skip"


            recommendations.append(
                recommendation
            )


        recommendations.sort(
            key=lambda x: x["match_score"],
            reverse=True,
        )

        return recommendations