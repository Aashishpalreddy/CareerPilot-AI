from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.core.security import get_current_user
from backend.app.models.user import User

from backend.app.repositories.parsed_job_repository import (
    ParsedJobRepository,
)
from backend.app.repositories.parsed_resume_repository import (
    ParsedResumeRepository,
)
from backend.app.repositories.tailored_resume_repository import (
    TailoredResumeRepository,
)

from backend.app.schemas.resume_tailor import (
    ResumeTailorResponse,
)

from backend.app.services.resume_tailor_service import (
    ResumeTailorService,
)

router = APIRouter(
    prefix="/resume-tailor",
    tags=["Resume Tailoring"],
)


@router.post(
    "/{resume_id}/{job_id}",
    response_model=ResumeTailorResponse,
)
def tailor_resume(
    resume_id: int,
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    parsed_resume = ParsedResumeRepository(
        db
    ).get_by_resume_id(
        resume_id
    )

    if parsed_resume is None:
        raise HTTPException(
            status_code=404,
            detail="Parsed resume not found.",
        )

    parsed_job = ParsedJobRepository(
        db
    ).get_by_job_id(
        job_id
    )

    if parsed_job is None:
        raise HTTPException(
            status_code=404,
            detail="Parsed job not found.",
        )

    service = ResumeTailorService(
        TailoredResumeRepository(db)
    )

    return service.tailor(
        parsed_resume,
        parsed_job,
    )