# Plan 004: Make CORS Origins Configurable

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md` — unless a reviewer dispatched you and told you they
> maintain the index.
>
> **Drift check (run first)**: `git diff --stat b8f4e2b..HEAD -- backend/app/main.py backend/app/core/config.py`
> If any in-scope file changed since this plan was written, compare the
> "Current state" excerpts against the live code before proceeding; on a
> mismatch, treat it as a STOP condition.

## Status

- **Priority**: P3
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none
- **Category**: tech-debt
- **Planned at**: commit `b8f4e2b`, 2026-07-16

## Why this matters

The FastAPI middleware in `backend/app/main.py` hardcodes `allow_origins` to `localhost:3000` and `3001`. This means when the backend is deployed to a staging or production environment, frontend clients on standard domains will be blocked by CORS policies. Moving this to an environment variable in `config.py` fixes this deployment blocker.

## Current state

- `backend/app/main.py:42`:
  ```python
  app.add_middleware(
      CORSMiddleware,
      allow_origins=[
          "http://localhost:3000",
          "http://127.0.0.1:3000",
          "http://localhost:3001",
          "http://127.0.0.1:3001",
      ],
  ```

## Commands you will need

| Purpose   | Command                  | Expected on success |
|-----------|--------------------------|---------------------|
| Syntax check| `python -m py_compile backend/app/main.py` | exit 0 |

## Scope

**In scope**:
- `backend/app/main.py`
- `backend/app/core/config.py`

**Out of scope**:
- Changing deployment infrastructure or dockerfiles.

## Git workflow

- Branch: `advisor/004-fix-dev-cors`
- Commit message: `fix: make CORS origins configurable via environment`

## Steps

### Step 1: Add CORS_ORIGINS to config.py
In `backend/app/core/config.py`, add a `BACKEND_CORS_ORIGINS` field to the Settings class (or equivalent). Default it to the existing localhost strings if possible. 

### Step 2: Use config in main.py
In `backend/app/main.py`, import the settings object (e.g., `from backend.app.core.config import settings`) and change `allow_origins` to use the configured array.

**Verify**: `python -m py_compile backend/app/main.py` → exits 0.

## Done criteria

- [ ] `allow_origins` in `main.py` reads from `settings`.
- [ ] Code has no syntax errors (`python -m py_compile backend/app/main.py`).
- [ ] No files outside the in-scope list are modified.
- [ ] `plans/README.md` status row updated.

## STOP conditions

Stop and report back if:
- `backend/app/core/config.py` doesn't exist or doesn't use `pydantic-settings`.
