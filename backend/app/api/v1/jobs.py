from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from backend.app.api.dependencies import (
    get_job_service,
    get_match_service,
    get_recommendation_service,
)

from backend.app.core.security import get_current_user
from backend.app.models.user import User

from backend.app.schemas.job import (
    JobCreate,
    JobResponse,
)

from backend.app.schemas.parsed_job import ParsedJobResponse
from backend.app.schemas.match import MatchResponse

from backend.app.services.job_service import JobService
from backend.app.services.match_service import MatchService
from backend.app.services.ai.recommendation_service import RecommendationService


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job(
    job: JobCreate,
    current_user: User = Depends(get_current_user),
    service: JobService = Depends(get_job_service),
):
    return service.create_job(
        current_user,
        job.raw_text,
    )


@router.get(
    "",
    response_model=list[JobResponse],
)
def get_jobs(
    current_user: User = Depends(get_current_user),
    service: JobService = Depends(get_job_service),
):
    return service.get_jobs(
        current_user,
    )


@router.get(
    "/{job_id}",
    response_model=JobResponse,
)
def get_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    service: JobService = Depends(get_job_service),
):
    job = service.get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    if job.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized",
        )

    return job


@router.post(
    "/{job_id}/parse",
    response_model=ParsedJobResponse,
)
def parse_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    service: JobService = Depends(get_job_service),
):
    job = service.get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    if job.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized",
        )

    return service.parse_job(job)


@router.post(
    "/{job_id}/match/{resume_id}",
    response_model=MatchResponse,
)
def match_resume_to_job(
    job_id: int,
    resume_id: int,
    current_user: User = Depends(get_current_user),
    job_service: JobService = Depends(get_job_service),
    match_service: MatchService = Depends(get_match_service),
):
    job = job_service.get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    if job.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized",
        )

    result = match_service.match_resume_to_job(
        resume_id=resume_id,
        job_id=job_id,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Parsed resume or parsed job not found",
        )

    return result


@router.post(
    "/recommend/{resume_id}",
)
def recommend_jobs(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    job_service: JobService = Depends(get_job_service),
    recommendation_service: RecommendationService = Depends(
        get_recommendation_service
    ),
):
    jobs = job_service.get_jobs(
        current_user,
    )

    job_ids = [
        job.id
        for job in jobs
    ]

    return recommendation_service.recommend_jobs(
        resume_id=resume_id,
        job_ids=job_ids,
    )


@router.delete(
    "/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    service: JobService = Depends(get_job_service),
):
    job = service.get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    if job.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized",
        )

    service.delete_job(job)