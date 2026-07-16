from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.core.security import get_current_user
from backend.app.models.user import User

from backend.app.repositories.resume_repository import (
    ResumeRepository,
)
from backend.app.repositories.parsed_resume_repository import (
    ParsedResumeRepository,
)
from backend.app.repositories.tailored_resume_repository import (
    TailoredResumeRepository,
)

from backend.app.schemas.generated_resume import (
    GeneratedResumeResponse,
)

from backend.app.services.docx_resume_service import (
    DocxResumeService,
)

router = APIRouter(
    prefix="/generated-resume",
    tags=["Generated Resume"],
)

GENERATED_DIR = Path("generated_resumes")


@router.post(
    "/{resume_id}/{job_id}",
    response_model=GeneratedResumeResponse,
)
def generate_resume(
    resume_id: int,
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    resume = ResumeRepository(db).get_by_id(resume_id)

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

    parsed_resume = ParsedResumeRepository(db).get_by_resume_id(resume_id)

    if parsed_resume is None:
        raise HTTPException(
            status_code=404,
            detail="Parsed resume not found.",
        )

    tailored = TailoredResumeRepository(db).get(resume_id, job_id)

    if tailored is None:
        raise HTTPException(
            status_code=404,
            detail="Tailored resume not found.",
        )

    output = DocxResumeService.generate(
        resume=resume,
        parsed_resume=parsed_resume,
        tailored_resume=tailored,
    )

    filename = Path(output).name

    return GeneratedResumeResponse(
        resume_id=resume_id,
        job_id=job_id,
        output_path=output,
        download_url=f"/generated-resume/download/{filename}",
    )


@router.get(
    "/download/{filename}",
)
def download_resume(
    filename: str,
    current_user: User = Depends(get_current_user),
):
    # Sanitize: reject any path separators to prevent traversal
    if "/" in filename or "\\" in filename or ".." in filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename.",
        )

    file_path = (GENERATED_DIR / filename).resolve()

    # Verify the resolved path stays within the allowed directory
    if not str(file_path).startswith(str(GENERATED_DIR.resolve())):
        raise HTTPException(
            status_code=400,
            detail="Invalid filename.",
        )

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found.",
        )

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )