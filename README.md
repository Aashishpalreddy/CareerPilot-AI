# CareerPilot AI

An AI-powered career platform that automates job discovery, resume optimization,
recruiter outreach, and application management using a multi-agent AI architecture.

Upload a resume, and CareerPilot parses it, scores it against ATS heuristics,
discovers matching jobs from public providers, tailors your resume and cover
letter to each role, and can prepare applications automatically.

---

## Tech Stack

| Layer      | Technology                                                                      |
| ---------- | ------------------------------------------------------------------------------- |
| Backend    | Python 3.11, FastAPI, SQLAlchemy ORM, Alembic (migrations), APScheduler         |
| Database   | PostgreSQL 16                                                                    |
| Frontend   | Next.js (React 19, TypeScript), Tailwind CSS, shadcn/ui, TanStack Query          |
| AI         | Anthropic Claude API (wrapped in a single `LLMClient`), with heuristic fallbacks |
| Automation | Playwright (optional, for auto-apply browser flows)                             |

---

## Quick Start (Docker)

The fastest way to run the whole stack (Postgres + backend + frontend):

```bash
cp .env.example .env          # then edit secrets (SECRET_KEY, ANTHROPIC_API_KEY, ...)
docker compose up --build
```

- Frontend: <http://localhost:3000>
- API:      <http://localhost:8000>  (interactive docs at `/docs`)

The backend container waits for Postgres, runs Alembic migrations, and then
starts the API automatically.

> **Note:** `NEXT_PUBLIC_API_URL` is baked into the frontend at build time
> because the browser (not the container) calls the API. It defaults to
> `http://localhost:8000`; override it via the same variable in `.env` if you
> deploy the backend elsewhere.

---

## Local Development (without Docker)

### Prerequisites

- Python 3.11+
- Node.js 20+
- A running PostgreSQL 16 instance

### Backend

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env          # fill in DB creds + SECRET_KEY
createdb careerpilot          # or create the DB however you prefer

alembic upgrade head          # apply migrations
uvicorn backend.app.main:app --reload
```

The API runs at <http://localhost:8000>.

### Frontend

```bash
cd frontend
cp .env.example .env.local     # NEXT_PUBLIC_API_URL=http://localhost:8000
npm install
npm run dev
```

The app runs at <http://localhost:3000>.

---

## Environment Variables

Backend (`.env`, see `.env.example`):

| Variable                        | Required | Description                                                        |
| ------------------------------- | -------- | ------------------------------------------------------------------ |
| `DEBUG`                         | no       | `True` enables SQL echo/verbose logging. Default `False`.          |
| `DB_HOST` / `DB_PORT`           | yes      | PostgreSQL host and port.                                          |
| `DB_NAME` / `DB_USER` / `DB_PASSWORD` | yes | PostgreSQL database and credentials.                               |
| `SECRET_KEY`                    | yes      | JWT signing secret. Use a long random value in production.         |
| `ALGORITHM`                     | no       | JWT algorithm. Default `HS256`.                                    |
| `ACCESS_TOKEN_EXPIRE_MINUTES`   | no       | Access-token lifetime. Default `30`.                              |
| `ANTHROPIC_API_KEY`             | no       | Anthropic Claude key. If blank, AI features use heuristic fallbacks. |
| `ANTHROPIC_MODEL`               | no       | Claude model ID. Default `claude-opus-4-8`.                        |
| `DAILY_PIPELINE_INTERVAL_HOURS` | no       | How often the discovery/tailoring pipeline runs. Default `24`.     |
| `BACKEND_CORS_ORIGINS`          | no       | JSON array of allowed frontend origins.                            |

Frontend (`frontend/.env.local`):

| Variable              | Description                                                    |
| --------------------- | ------------------------------------------------------------- |
| `NEXT_PUBLIC_API_URL` | Backend origin (no `/api/v1` suffix). Default `http://localhost:8000`. |

---

## Core Features

- **Resume Management** — upload PDF/DOCX, AI-extract structured data
  (`AIResumeParser` → `ParsedResume`), with a heuristic parser fallback when
  no AI key is configured.
- **ATS Analyzer** — `ATSScoreService` returns a score out of 100 with
  strengths, weaknesses, and suggestions. Falls back to a deterministic
  heuristic score when the Claude quota is exhausted (and does not cache the
  fallback, so a real score can be fetched later).
- **Job Discovery Pipeline** — `DailyPipelineService` fetches jobs from
  providers (Greenhouse, RemoteOK), matches them against the default resume,
  and tailors resume + cover letter for strong matches.
- **Auto Apply** — `AutoApplyService` prepares/submits applications for
  eligible jobs using tailored materials.
- **Dashboard** — manage resumes, view ATS scores, and track saved jobs
  through `saved` / `applied` / `dismissed` states.

---

## Testing

```bash
source .venv/bin/activate
pytest
```

Smoke tests verify the app imports, core routes are registered, and the
resume-parsing helpers behave — the classes of regression that previously
broke startup.

---

## Project Structure

```
backend/
  app/
    api/v1/          FastAPI routers (auth, resumes, jobs, apply, ...)
    core/            config, security, scheduler
    database/        SQLAlchemy engine + session
    integrations/    external job providers (greenhouse, remoteok)
    models/          SQLAlchemy models
    repositories/    data-access layer
    schemas/         Pydantic request/response models
    services/        business logic (incl. services/ai for LLM features)
  migrations/        Alembic migrations
frontend/
  src/
    app/             Next.js App Router pages
    components/       UI + feature components
    hooks/            TanStack Query hooks
    services/         API client layer
docker-compose.yml   Postgres + backend + frontend
Dockerfile           Backend image
frontend/Dockerfile  Frontend image
```
