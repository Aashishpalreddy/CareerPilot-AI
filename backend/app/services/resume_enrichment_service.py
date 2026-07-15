import logging

from backend.app.models.parsed_resume import ParsedResume
from backend.app.repositories.parsed_resume_repository import (
    ParsedResumeRepository,
)
from backend.app.services.ai_resume_parser import AIResumeParser

logger = logging.getLogger(__name__)


class ResumeEnrichmentService:
    """
    Enriches a ParsedResume using Claude AI.

    Existing rule-based parsing remains intact.
    AI simply adds richer structured information.
    """

    def __init__(
        self,
        repository: ParsedResumeRepository,
    ):
        self.repository = repository
        self.ai_parser = AIResumeParser()

    def enrich(
        self,
        parsed_resume: ParsedResume,
    ) -> ParsedResume:

        try:

            profile = self.ai_parser.parse(
                parsed_resume.raw_text
            )

            parsed_resume.summary = profile.summary

            parsed_resume.skills = profile.skills

            parsed_resume.experience = [
                exp.model_dump()
                for exp in profile.experience
            ]

            parsed_resume.education = [
                edu.model_dump()
                for edu in profile.education
            ]

            parsed_resume.projects = [
                project.model_dump()
                for project in profile.projects
            ]

            parsed_resume.certifications = [
                cert.model_dump()
                for cert in profile.certifications
            ]

            parsed_resume.technologies = (
                profile.technologies
            )

            parsed_resume.languages = (
                profile.languages
            )

            parsed_resume.achievements = (
                profile.achievements
            )

            parsed_resume.years_experience = (
                profile.years_experience
            )

            return self.repository.update(
                parsed_resume
            )

        except Exception as e:

            logger.exception(
                "Resume AI enrichment failed."
            )

            # Keep the existing parsed resume instead
            return parsed_resume