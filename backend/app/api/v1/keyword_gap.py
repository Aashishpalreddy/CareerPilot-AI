from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.repositories.parsed_job_repository import ParsedJobRepository
from backend.app.repositories.parsed_resume_repository import ParsedResumeRepository
from backend.app.schemas.keyword_gap import KeywordGapResponse
from backend.app.services.keyword_gap_service import KeywordGapService

router = APIRouter(
    prefix="/keyword-gap",
    tags=["Keyword Gap Analysis"],
)


@router.get(
    "/{resume_id}/{job_id}",
    response_model=KeywordGapResponse,
)
def analyze_keyword_gap(
    resume_id: int,
    job_id: int,
    db: Session = Depends(get_db),
):

    parsed_resume_repository = ParsedResumeRepository(db)
    parsed_job_repository = ParsedJobRepository(db)

    parsed_resume = parsed_resume_repository.get_by_resume_id(
        resume_id
    )

    if parsed_resume is None:
        raise HTTPException(
            status_code=404,
            detail="Parsed resume not found.",
        )

    parsed_job = parsed_job_repository.get_by_job_id(
        job_id
    )

    if parsed_job is None:
        raise HTTPException(
            status_code=404,
            detail="Parsed job not found.",
        )

    service = KeywordGapService()

    return service.analyze(
        parsed_resume,
        parsed_job,
    )