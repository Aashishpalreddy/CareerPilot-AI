# Plan 001: Use real user data in AutoApplyService

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md` — unless a reviewer dispatched you and told you they
> maintain the index.
>
> **Drift check (run first)**: `git diff --stat b8f4e2b..HEAD -- backend/app/services/ai/daily_pipeline_service.py`
> If any in-scope file changed since this plan was written, compare the
> "Current state" excerpts against the live code before proceeding; on a
> mismatch, treat it as a STOP condition.

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none
- **Category**: correctness
- **Planned at**: commit `b8f4e2b`, 2026-07-16

## Why this matters

The `DailyPipelineService` hardcodes the auto-apply user data to "Test User" instead of fetching it from the database. This means when a real user runs the pipeline and a job is eligible for auto-apply, the system applies with fake data. Fixing this ensures the actual user's details are sent with their job application.

## Current state

- `backend/app/services/ai/daily_pipeline_service.py` — The core pipeline loop for discovering and auto-applying to jobs. Lines 145-149 contain the hardcoded info:
  ```python
  user_info = {
      "first_name": "Test",
      "last_name": "User",
      "email": "test@example.com",
      "phone": "1234567890"
  }
  ```
- Error handling follows standard Python try-except logging.

## Commands you will need

| Purpose   | Command                  | Expected on success |
|-----------|--------------------------|---------------------|
| Syntax check| `python -m py_compile backend/app/services/ai/daily_pipeline_service.py` | exit 0 |

## Scope

**In scope**:
- `backend/app/services/ai/daily_pipeline_service.py`

**Out of scope**:
- `backend/app/services/ai/auto_apply_service.py` (do not touch)

## Git workflow

- Branch: `advisor/001-fix-autoapply-user-data`
- Commit message: `fix: use real user data for auto apply in daily pipeline`

## Steps

### Step 1: Fetch user from the database
The `DailyPipelineService.run_for_user` method receives a `user_id`. You must use the database session (`self.db`) to fetch the `User` object. Add `from backend.app.models.user import User` to the top of the file if needed.
Then, near line 69 where `self.resume_repository.get_default(user_id)` is called, also query for the user:
`user = self.db.query(User).filter(User.id == user_id).first()`
If the user is None, you can return early or handle it appropriately.

**Verify**: `python -m py_compile backend/app/services/ai/daily_pipeline_service.py` → exits 0

### Step 2: Replace hardcoded dictionary
Replace the hardcoded `user_info` dictionary (around line 145) with the fields from the fetched `User` object:
```python
user_info = {
    "first_name": user.first_name,
    "last_name": user.last_name,
    "email": user.email,
    "phone": getattr(user, "phone", "1234567890")
}
```
*(Assuming `User` model has these fields; fallback on phone if missing).*

**Verify**: `python -m py_compile backend/app/services/ai/daily_pipeline_service.py` → exits 0

## Test plan

- Test coverage is currently zero across the backend (see plan 002). Rely on visual inspection and `python -m py_compile`.

## Done criteria

- [ ] `user_info` dictionary in `backend/app/services/ai/daily_pipeline_service.py` pulls from the DB user.
- [ ] Code has no syntax errors (`python -m py_compile backend/app/services/ai/daily_pipeline_service.py`).
- [ ] No files outside the in-scope list are modified (`git status`).
- [ ] `plans/README.md` status row updated.

## STOP conditions

Stop and report back (do not improvise) if:
- The hardcoded "Test User" dictionary is no longer at line 145-149.
- You cannot locate a `User` model import or it doesn't have the necessary fields (`first_name`, `last_name`, `email`).

## Maintenance notes
- Future changes that add more robust user profiles may require updating `user_info` here to include location, LinkedIn URL, etc.
