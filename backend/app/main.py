import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.users import router as users_router
from backend.app.api.v1.resumes import router as resumes_router
from backend.app.api.v1.jobs import router as job_router
from backend.app.api.v1.job_search import router as job_search_router
from backend.app.api.v1.apply import router as apply_router
from backend.app.api.v1.keyword_gap import router as keyword_gap_router
from backend.app.api.v1.resume_match import router as resume_match_router
from backend.app.api.v1.resume_tailor import router as resume_tailor_router
from backend.app.api.v1.generated_resume import router as generated_resume_router
from backend.app.api.v1.cover_letter import router as cover_letter_router

from backend.app.core.config import settings
from backend.app.core.scheduler import start_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Startup / shutdown lifecycle using the modern lifespan pattern."""
    start_scheduler()
    yield


app = FastAPI(
    title="CareerPilot AI",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── All routers registered together ──────────────────────────────────
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(resumes_router)
app.include_router(job_router)
app.include_router(job_search_router)
app.include_router(apply_router)
app.include_router(keyword_gap_router)
app.include_router(resume_match_router)
app.include_router(resume_tailor_router)
app.include_router(generated_resume_router)
app.include_router(cover_letter_router)


@app.get("/")
def root():
    return {"message": "CareerPilot AI API"}


@app.get("/health")
def health():
    return {"status": "healthy"}