from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.database.session import get_db

from backend.app.repositories.resume_repository import ResumeRepository
from backend.app.repositories.parsed_resume_repository import ParsedResumeRepository

from backend.app.repositories.job_repository import JobRepository
from backend.app.repositories.parsed_job_repository import ParsedJobRepository

from backend.app.services.resume_service import ResumeService
from backend.app.services.job_service import JobService
from backend.app.services.parsed_job_service import ParsedJobService

from backend.app.services.match_service import MatchService
from backend.app.services.ai.recommendation_service import RecommendationService

from backend.app.repositories.saved_job_repository import SavedJobRepository
from backend.app.services.ai.daily_pipeline_service import DailyPipelineService


def get_resume_service(
    db: Session = Depends(get_db),
) -> ResumeService:

    resume_repository = ResumeRepository(db)
    parsed_resume_repository = ParsedResumeRepository(db)

    return ResumeService(
        repository=resume_repository,
        parsed_repository=parsed_resume_repository,
    )


def get_parsed_job_service(
    db: Session = Depends(get_db),
) -> ParsedJobService:

    parsed_job_repository = ParsedJobRepository(db)

    return ParsedJobService(
        repository=parsed_job_repository,
    )


def get_job_service(
    db: Session = Depends(get_db),
) -> JobService:

    job_repository = JobRepository(db)

    parsed_job_repository = ParsedJobRepository(db)

    parsed_job_service = ParsedJobService(
        repository=parsed_job_repository,
    )

    return JobService(
        repository=job_repository,
        parsed_service=parsed_job_service,
    )


def get_match_service(
    db: Session = Depends(get_db),
) -> MatchService:

    parsed_resume_repository = ParsedResumeRepository(db)
    parsed_job_repository = ParsedJobRepository(db)

    return MatchService(
        parsed_resume_repository=parsed_resume_repository,
        parsed_job_repository=parsed_job_repository,
    )


def get_recommendation_service(
    db: Session = Depends(get_db),
) -> RecommendationService:

    parsed_resume_repository = ParsedResumeRepository(db)
    parsed_job_repository = ParsedJobRepository(db)

    match_service = MatchService(
        parsed_resume_repository=parsed_resume_repository,
        parsed_job_repository=parsed_job_repository,
    )

    return RecommendationService(
        match_service=match_service,
    )


def get_saved_job_repository(
    db: Session = Depends(get_db),
) -> SavedJobRepository:

    return SavedJobRepository(db)


def get_daily_pipeline_service(
    db: Session = Depends(get_db),
) -> DailyPipelineService:

    return DailyPipelineService(db)