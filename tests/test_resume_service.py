"""Unit test for the fallback (non-AI) resume parsing path, which must
flatten the categorized skill dict into a flat list[str] so it satisfies
the ParsedResume response schema."""

from backend.app.services.resume_intelligence_service import (
    ResumeIntelligenceService,
)


def test_extract_skills_returns_categorized_dict():
    result = ResumeIntelligenceService.extract_skills(
        ["Python, SQL, Docker, FastAPI"]
    )
    assert isinstance(result, dict)
    flat = [s for group in result.values() for s in group]
    assert "Python" in flat
    assert "Docker" in flat
    # Flattening (as ResumeService does) must yield a list of strings.
    assert all(isinstance(s, str) for s in flat)
