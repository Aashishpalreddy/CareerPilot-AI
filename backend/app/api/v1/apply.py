from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from backend.app.api.dependencies import (
    get_daily_pipeline_service,
    get_saved_job_repository,
)
from backend.app.core.security import get_current_user
from backend.app.models.user import User
from backend.app.repositories.saved_job_repository import SavedJobRepository
from backend.app.schemas.saved_job import SavedJobResponse, SavedJobSummary
from backend.app.services.ai.daily_pipeline_service import DailyPipelineService

router = APIRouter(prefix="/apply", tags=["Apply"])


class RunPipelineRequest(BaseModel):
    keywords: list[str]
    location: str | None = None
    remote_only: bool = False


@router.post("/run", response_model=list[SavedJobResponse])
async def run_daily_pipeline(
    request: RunPipelineRequest,
    current_user: User = Depends(get_current_user),
    pipeline: DailyPipelineService = Depends(get_daily_pipeline_service),
):
    """
    Runs discovery + matching + tailoring for the current user right now.
    In production this same call is what the daily scheduler triggers.
    """

    return await pipeline.run_for_user(
        user_id=current_user.id,
        keywords=request.keywords,
        location=request.location,
        remote_only=request.remote_only,
    )


@router.get("/saved-jobs", response_model=list[SavedJobSummary])
def list_saved_jobs(
    status_filter: str | None = None,
    current_user: User = Depends(get_current_user),
    repository: SavedJobRepository = Depends(get_saved_job_repository),
):
    return repository.get_by_user(
        user_id=current_user.id,
        status=status_filter,
    )


@router.get("/saved-jobs/{saved_job_id}", response_model=SavedJobResponse)
def get_saved_job(
    saved_job_id: int,
    current_user: User = Depends(get_current_user),
    repository: SavedJobRepository = Depends(get_saved_job_repository),
):
    saved_job = repository.get_by_id(saved_job_id)

    if saved_job is None:
        raise HTTPException(status_code=404, detail="Saved job not found")

    if saved_job.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return saved_job


@router.post(
    "/saved-jobs/{saved_job_id}/mark-applied",
    response_model=SavedJobResponse,
)
def mark_applied(
    saved_job_id: int,
    current_user: User = Depends(get_current_user),
    repository: SavedJobRepository = Depends(get_saved_job_repository),
):
    saved_job = repository.get_by_id(saved_job_id)

    if saved_job is None:
        raise HTTPException(status_code=404, detail="Saved job not found")

    if saved_job.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return repository.mark_applied(saved_job)


@router.delete(
    "/saved-jobs/{saved_job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def dismiss_saved_job(
    saved_job_id: int,
    current_user: User = Depends(get_current_user),
    repository: SavedJobRepository = Depends(get_saved_job_repository),
):
    saved_job = repository.get_by_id(saved_job_id)

    if saved_job is None:
        raise HTTPException(status_code=404, detail="Saved job not found")

    if saved_job.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    repository.delete(saved_job)