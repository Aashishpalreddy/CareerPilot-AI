from backend.app.repositories.cover_letter_repository import (
    CoverLetterRepository,
)
from backend.app.services.document_generator import (
    DocumentGenerator,
)


class CoverLetterService:

    def __init__(
        self,
        cover_letter_repository: CoverLetterRepository,
    ):
        self.cover_letter_repository = cover_letter_repository
        self.document_generator = DocumentGenerator()

    def generate_docx(
        self,
        cover_letter_id: int,
    ) -> str:

        cover_letter = self.cover_letter_repository.get_by_id(
            cover_letter_id
        )

        if cover_letter is None:
            raise ValueError("Cover letter not found.")

        filename = self.document_generator.generate_cover_letter(
            applicant_name=cover_letter.user.full_name,
            applicant_email=cover_letter.user.email,
            company=cover_letter.company,
            position=cover_letter.position,
            content=cover_letter.content,
        )

        cover_letter.docx_filename = filename

        self.cover_letter_repository.update(
            cover_letter
        )

        return filename