"""Smoke tests that guard against import-time and router-registration
regressions (the class of breakage that previously stopped the app booting).
These do not require a database connection."""

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_app_imports_and_root_responds():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "CareerPilot AI API"}


def test_core_routes_are_registered():
    paths = set(app.openapi()["paths"].keys())
    expected = {
        "/auth/login",
        "/auth/register",
        "/users/me",
        "/resumes",
        "/resumes/upload",
        "/resumes/{resume_id}/ats",
        "/jobs",
        "/apply/saved-jobs",
    }
    missing = expected - paths
    assert not missing, f"Missing registered routes: {missing}"
