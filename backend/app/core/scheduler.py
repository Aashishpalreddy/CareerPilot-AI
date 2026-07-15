import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from backend.app.core.config import settings
from backend.app.database.session import SessionLocal
from backend.app.models.resume import Resume
from backend.app.models.user import User
from backend.app.repositories.parsed_resume_repository import ParsedResumeRepository
from backend.app.services.ai.daily_pipeline_service import DailyPipelineService

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

# How many top skills from the resume to use as search keywords.
KEYWORDS_PER_USER = 8


def _extract_keywords(skills) -> list[str]:
    if isinstance(skills, dict):
        flat = [s for group in skills.values() if isinstance(group, list) for s in group]
        return flat[:KEYWORDS_PER_USER]

    if isinstance(skills, list):
        return skills[:KEYWORDS_PER_USER]

    return []


async def run_daily_pipeline_for_all_users() -> None:
    """
    Entry point invoked once a day by the scheduler. Every user with a
    default resume gets discovery + matching + tailoring run against
    keywords pulled from that resume's parsed skills.
    """

    db = SessionLocal()

    try:
        users = db.query(User).filter(User.is_active.is_(True)).all()

        parsed_resume_repository = ParsedResumeRepository(db)

        for user in users:

            default_resume = (
                db.query(Resume)
                .filter(Resume.user_id == user.id, Resume.is_default.is_(True))
                .first()
            )

            if default_resume is None:
                continue

            parsed_resume = parsed_resume_repository.get_by_resume_id(
                default_resume.id
            )

            if parsed_resume is None:
                logger.info(
                    "User %s's default resume isn't parsed yet; skipping.",
                    user.id,
                )
                continue

            keywords = _extract_keywords(parsed_resume.skills)

            if not keywords:
                logger.info(
                    "No skills extracted for user %s; skipping daily run.",
                    user.id,
                )
                continue

            pipeline = DailyPipelineService(db)

            try:
                saved = await pipeline.run_for_user(
                    user_id=user.id,
                    keywords=keywords,
                )

                logger.info(
                    "Daily pipeline for user %s saved %d new jobs.",
                    user.id,
                    len(saved),
                )

            except Exception:
                logger.exception(
                    "Daily pipeline failed for user %s",
                    user.id,
                )

    finally:
        db.close()


def start_scheduler() -> None:
    scheduler.add_job(
        run_daily_pipeline_for_all_users,
        "interval",
        hours=settings.DAILY_PIPELINE_INTERVAL_HOURS,
        id="daily_job_pipeline",
        replace_existing=True,
    )
    scheduler.start()
    logger.info(
        "Daily job pipeline scheduled every %s hour(s).",
        settings.DAILY_PIPELINE_INTERVAL_HOURS,
    )
