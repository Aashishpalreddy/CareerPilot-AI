from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.models.user import User
from backend.app.core.security import get_current_user
from backend.app.services.ai.job_discovery_service import JobDiscoveryService


router = APIRouter(
    prefix="/job-search",
    tags=["Job Search"],
)


class JobSearchRequest(BaseModel):
    keywords: list[str]
    location: str | None = None
    remote_only: bool = False
    job_type: str | None = None
    experience_level: str | None = None
    max_results: int = 50


def get_job_discovery_service(
    db: Session = Depends(get_db),
) -> JobDiscoveryService:

    return JobDiscoveryService(
        db=db,
    )


@router.post("/")
async def search_jobs(
    request: JobSearchRequest,
    current_user: User = Depends(get_current_user),
    service: JobDiscoveryService = Depends(
        get_job_discovery_service
    ),
):

    jobs = await service.discover_and_save_jobs(
        user_id=current_user.id,
        keywords=request.keywords,
        location=request.location,
        remote_only=request.remote_only,
        job_type=request.job_type,
        experience_level=request.experience_level,
        max_results_per_provider=request.max_results,
    )

    return {
        "total_jobs": len(jobs),
        "jobs": jobs,
    }