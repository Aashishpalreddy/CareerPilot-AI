from fastapi import FastAPI

from backend.app.api.v1.auth import router as auth_router

app = FastAPI(
    title="CareerPilot AI",
    version="1.0.0",
)

app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "CareerPilot AI API"}


@app.get("/health")
def health():
    return {"status": "healthy"}