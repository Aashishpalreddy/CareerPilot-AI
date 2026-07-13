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
from pathlib import Path
from sqlalchemy.orm import Session

from backend.app.core.security import get_current_user
from backend.app.database.session import get_db
from backend.app.models.user import User
from backend.app.repositories.resume_repository import ResumeRepository
from backend.app.schemas.resume import ResumeCreate, ResumeResponse
from backend.app.services.resume_service import ResumeService
from backend.app.utils.file_handler import save_resume


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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = ResumeRepository(db)
    service = ResumeService(repository)

    return service.create_resume(
        current_user,
        resume,
    )


@router.post(
    "/upload",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_resume(
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = ResumeRepository(db)
    service = ResumeService(repository)

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

    return service.create_resume(
        current_user,
        resume,
    )


@router.get(
    "",
    response_model=list[ResumeResponse],
)
def get_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = ResumeRepository(db)
    service = ResumeService(repository)

    return service.get_resumes(current_user)


@router.get(
    "/{resume_id}",
    response_model=ResumeResponse,
)
def get_resume(
    resume_id: int,
    db: Session = Depends(get_db),
):
    repository = ResumeRepository(db)
    service = ResumeService(repository)

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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = ResumeRepository(db)
    service = ResumeService(repository)

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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = ResumeRepository(db)
    service = ResumeService(repository)

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
    db: Session = Depends(get_db),
):
    repository = ResumeRepository(db)
    service = ResumeService(repository)

    resume = service.get_resume(resume_id)

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    service.delete_resume(resume)