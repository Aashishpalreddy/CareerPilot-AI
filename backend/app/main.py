from fastapi import FastAPI

from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.users import router as users_router
from backend.app.api.v1.resumes import router as resumes_router

app = FastAPI(
    title="CareerPilot AI",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(resumes_router)


@app.get("/")
def root():
    return {
        "message": "CareerPilot AI API",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }