import asyncio
import logging
from backend.app.database.session import SessionLocal
from backend.app.repositories.resume_repository import ResumeRepository
from backend.app.services.resume_service import ResumeService
from backend.app.repositories.parsed_resume_repository import ParsedResumeRepository

logging.basicConfig(level=logging.DEBUG)

def test_ats():
    db = SessionLocal()
    try:
        resume_repo = ResumeRepository(db)
        parsed_repo = ParsedResumeRepository(db)
        service = ResumeService(resume_repo, parsed_repo)
        
        # Get first resume
        resumes = resume_repo.get_by_user(5) # I saw user 5 in earlier logs
        if not resumes:
            print("No resumes found for user 5")
            resumes = db.query(resume_repo.model).all()
            if not resumes:
                print("No resumes in DB")
                return
        resume = resumes[0]
        
        print("Testing ATS Score for resume:", resume.id)
        result = service.get_ats_score(resume)
        print("Result:", result)
        
    finally:
        db.close()

if __name__ == "__main__":
    test_ats()
