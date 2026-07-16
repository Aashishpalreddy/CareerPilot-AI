# Plan 002: Establish Verification Baseline

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md` — unless a reviewer dispatched you and told you they
> maintain the index.
>
> **Drift check (run first)**: `git diff --stat b8f4e2b..HEAD -- backend/requirements.txt`
> If any in-scope file changed since this plan was written, compare the
> "Current state" excerpts against the live code before proceeding; on a
> mismatch, treat it as a STOP condition.

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: LOW
- **Depends on**: none
- **Category**: tests
- **Planned at**: commit `b8f4e2b`, 2026-07-16

## Why this matters

The `tests/` directory is completely empty and no test runner (`pytest`) is included in the project's dependencies. This creates a critical lack of a verification baseline. Without tests, any subsequent refactors or features carry a high risk of breaking existing functionality silently.

## Current state

- `backend/requirements/base.txt` and `requirements.txt` lack test libraries.
- `tests/` directory is present but completely empty.

## Commands you will need

| Purpose   | Command                  | Expected on success |
|-----------|--------------------------|---------------------|
| Run tests | `pytest tests/`          | exit 0, all pass    |

## Scope

**In scope**:
- `requirements.txt`
- `tests/conftest.py` (create)
- `tests/test_health.py` (create)

**Out of scope**:
- Writing comprehensive unit tests for all services. (This is just to establish the baseline).

## Git workflow

- Branch: `advisor/002-add-verification-baseline`
- Commit message: `test: establish pytest verification baseline`

## Steps

### Step 1: Add pytest dependencies
Add `pytest`, `pytest-asyncio`, and `httpx` (for FastAPI test client) to the main `requirements.txt` (or create a `backend/requirements/test.txt` if that's the convention, but to be simple, add them to `requirements.txt` at the root).

**Verify**: `pip install pytest pytest-asyncio httpx` succeeds.

### Step 2: Create a basic test for the health endpoint
Create `tests/test_health.py` and write a basic test for the FastAPI `/health` endpoint defined in `backend/app/main.py`.
```python
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
```

**Verify**: `pytest tests/test_health.py` exits 0.

## Test plan

- You are writing the tests themselves. 
- Verification: `pytest tests/` → all pass.

## Done criteria

- [ ] `pytest`, `pytest-asyncio`, `httpx` are in `requirements.txt`.
- [ ] `tests/test_health.py` exists and correctly asserts the `/health` endpoint.
- [ ] `pytest tests/` runs and exits 0.
- [ ] `plans/README.md` status row updated.

## STOP conditions

Stop and report back (do not improvise) if:
- `pytest` fails to discover the tests because of import path issues (you might need to create `tests/__init__.py`).
- The `app` fixture cannot be imported due to complex DB dependencies at startup.

## Maintenance notes
- Once this is merged, require all future PRs (and plans) to run tests in CI.
