from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    BackgroundTasks,
    status,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import asyncio

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


async def process_new_resume_background(user_id: int, resume_id: int):
    from backend.app.database.session import SessionLocal
    from backend.app.repositories.resume_repository import ResumeRepository
    from backend.app.repositories.parsed_resume_repository import ParsedResumeRepository
    from backend.app.services.ai.daily_pipeline_service import DailyPipelineService
    
    db = SessionLocal()
    try:
        resume_repo = ResumeRepository(db)
        parsed_repo = ParsedResumeRepository(db)
        resume_service = ResumeService(resume_repo, parsed_repo)
        
        resume = resume_repo.get_by_id(resume_id)
        if not resume:
            return
            
        # 1. Parse the resume
        parsed_resume = resume_service.parse_resume(resume)
        
        # 2. Extract skills to use as keywords
        keywords = parsed_resume.skills[:5] if parsed_resume.skills else []
        if not keywords:
            keywords = ["Software Engineer"]
            
        # 3. Run job discovery pipeline
        pipeline = DailyPipelineService(db)
        await pipeline.run_for_user(
            user_id=user_id,
            keywords=keywords,
        )
    except Exception as e:
        import logging
        logging.getLogger(__name__).exception("Background processing failed")
    finally:
        db.close()


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
    background_tasks: BackgroundTasks,
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

    resume_data = ResumeCreate(
        title=title,
        original_filename=uploaded["original_filename"],
        file_path=uploaded["filepath"],
    )

    created_resume = service.create_resume(current_user, resume_data)
    
    background_tasks.add_task(
        process_new_resume_background,
        user_id=current_user.id,
        resume_id=created_resume.id
    )

    return created_resume


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
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service),
    db: Session = Depends(get_db),
):
    resume = service.get_resume(resume_id)

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found.",
        )

    if resume.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized",
        )

    parsed = ParsedResumeRepository(db).get_by_resume_id(
        resume_id
    )

    if parsed is None:
        raise HTTPException(
            status_code=404,
            detail="Parsed resume not found.",
        )

    return parsed