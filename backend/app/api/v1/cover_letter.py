from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from backend.app.database.session import get_db

from backend.app.models.cover_letter import CoverLetter

from backend.app.repositories.cover_letter_repository import (
    CoverLetterRepository,
)
from backend.app.repositories.parsed_job_repository import (
    ParsedJobRepository,
)
from backend.app.repositories.parsed_resume_repository import (
    ParsedResumeRepository,
)
from backend.app.repositories.resume_repository import (
    ResumeRepository,
)

from backend.app.schemas.cover_letter import (
    CoverLetterResponse,
)

from backend.app.services.ai.cover_letter_service import (
    CoverLetterService,
)

from backend.app.services.cover_letter_service import (
    CoverLetterService as CoverLetterDocumentService,
)

router = APIRouter(
    prefix="/cover-letter",
    tags=["Cover Letter"],
)


@router.post(
    "/generate/{resume_id}/{job_id}",
)
def generate_cover_letter(
    resume_id: int,
    job_id: int,
    db: Session = Depends(get_db),
):

    resume = ResumeRepository(db).get_by_id(
        resume_id
    )

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found.",
        )

    parsed_resume = ParsedResumeRepository(db).get_by_resume_id(
        resume_id
    )

    if parsed_resume is None:
        raise HTTPException(
            status_code=404,
            detail="Parsed resume not found.",
        )

    parsed_job = ParsedJobRepository(db).get_by_job_id(
        job_id
    )

    if parsed_job is None:
        raise HTTPException(
            status_code=404,
            detail="Parsed job not found.",
        )

    ai_service = CoverLetterService(
        ParsedResumeRepository(db),
        ParsedJobRepository(db),
    )

    generated = ai_service.generate_cover_letter(
        resume_id,
        job_id,
    )

    if generated is None:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate cover letter.",
        )

    cover_letter = CoverLetter(
        user_id=resume.user_id,
        resume_id=resume_id,
        job_id=job_id,
        company=parsed_job.company or "Unknown",
        position=parsed_job.title or "Unknown",
        content=generated.cover_letter_text,
    )

    saved = CoverLetterRepository(db).create(
        cover_letter
    )

    filename = CoverLetterDocumentService(
        CoverLetterRepository(db)
    ).generate_docx(
        saved.id
    )

    saved = CoverLetterRepository(db).get_by_id(
        saved.id
    )

    return {
        "id": saved.id,
        "resume_id": saved.resume_id,
        "job_id": saved.job_id,
        "company": saved.company,
        "position": saved.position,
        "content": saved.content,
        "docx_filename": filename,
        "pdf_filename": saved.pdf_filename,
        "status": saved.status,
        "created_at": saved.created_at,
        "download_url": f"/cover-letter/download/{filename}",
    }


@router.get(
    "/download/{filename}",
)
def download_cover_letter(
    filename: str,
):

    filepath = (
        Path("generated_documents/cover_letters")
        / filename
    )

    if not filepath.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found.",
        )

    return FileResponse(
        path=filepath,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )