import shutil
import uuid
from pathlib import Path

# Directory where resumes will be stored
UPLOAD_DIR = Path("uploads/resumes")

# Create directory if it doesn't exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Allowed file types
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}


def save_resume(upload_file):
    """
    Saves an uploaded resume to disk with a unique filename.

    Returns:
        dict containing:
        - filename
        - filepath
        - original_filename
    """

    extension = Path(upload_file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Only PDF, DOC, and DOCX files are allowed."
        )

    unique_filename = f"{uuid.uuid4()}{extension}"

    file_path = UPLOAD_DIR / unique_filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return {
        "filename": unique_filename,
        "filepath": str(file_path),
        "original_filename": upload_file.filename,
    }