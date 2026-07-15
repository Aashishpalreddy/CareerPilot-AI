from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.api.dependencies import get_resume_service
from backend.app.core.security import get_current_user
from backend.app.models.user import User
from backend.app.schemas.ats import ATSScoreResponse
from backend.app.schemas.parsed_resume import ParsedResumeResponse
from backend.app.schemas.resume import ResumeCreate, ResumeResponse
from backend.app.services.resume_service import ResumeService
from backend.app.utils.file_handler import save_resume

from backend.app.repositories.parsed_resume_repository import (
    ParsedResumeRepository,
)

router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"],
)


@router.post(
    "",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_resume(
    resume: ResumeCreate,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service),
):
    return service.create_resume(current_user, resume)


@router.post(
    "/upload",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_resume(
    title: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service),
):
    try:
        uploaded = save_resume(file)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    resume = ResumeCreate(
        title=title,
        original_filename=uploaded["original_filename"],
        file_path=uploaded["filepath"],
    )

    return service.create_resume(current_user, resume)


@router.get(
    "",
    response_model=list[ResumeResponse],
)
def get_resumes(
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service),
):
    return service.get_resumes(current_user)


@router.get(
    "/{resume_id}",
    response_model=ResumeResponse,
)
def get_resume(
    resume_id: int,
    service: ResumeService = Depends(get_resume_service),
):
    resume = service.get_resume(resume_id)

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    return resume


@router.patch(
    "/{resume_id}/default",
    response_model=ResumeResponse,
)
def set_default_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service),
):
    resume = service.get_resume(resume_id)

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    return service.set_default_resume(
        current_user,
        resume,
    )


@router.get(
    "/{resume_id}/download",
)
def download_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service),
):
    resume = service.get_resume(resume_id)

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    if resume.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized",
        )

    file_path = Path(resume.file_path)

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found",
        )

    return FileResponse(
        path=file_path,
        filename=resume.original_filename,
    )


@router.delete(
    "/{resume_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_resume(
    resume_id: int,
    service: ResumeService = Depends(get_resume_service),
):
    resume = service.get_resume(resume_id)

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    service.delete_resume(resume)


@router.post(
    "/{resume_id}/parse",
    response_model=ParsedResumeResponse,
)
def parse_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service),
):
    resume = service.get_resume(resume_id)

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    if resume.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized",
        )

    return service.parse_resume(resume)


@router.post(
    "/{resume_id}/ats",
    response_model=ATSScoreResponse,
)
def get_ats_score(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service),
):
    resume = service.get_resume(resume_id)

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    if resume.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized",
        )

    return service.get_ats_score(resume)


@router.get(
    "/parsed/{resume_id}",
)
def get_parsed_resume(
    resume_id: int,
    db: Session = Depends(get_db),
):
    parsed = ParsedResumeRepository(db).get_by_resume_id(
        resume_id
    )

    if parsed is None:
        raise HTTPException(
            status_code=404,
            detail="Parsed resume not found.",
        )

    return parsed