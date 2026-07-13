from fastapi import FastAPI

app = FastAPI(
    title="CareerPilot AI",
    description="AI-powered career platform for job discovery, resume optimization, interview preparation, and recruiter outreach.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to CareerPilot AI 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }