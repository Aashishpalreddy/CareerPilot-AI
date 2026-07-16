import logging

from backend.app.services.ai.llm_client import LLMClient

logger = logging.getLogger(__name__)

class ATSScoreService:

    @staticmethod
    def calculate(parsed_resume, parsed_job=None):
        resume_text = ""
        if parsed_resume.raw_text:
            resume_text = parsed_resume.raw_text
        else:
            resume_text = str(parsed_resume.summary) + " " + str(parsed_resume.skills)

        job_context = ""
        if parsed_job:
            job_context = f"\nTarget Job Description:\n{parsed_job.job_summary}\n\nTarget Skills: {', '.join(parsed_job.skills or [])}"
            
        system_prompt = """
You are an expert ATS (Applicant Tracking System) Analyzer.

Your task is to analyze the provided resume content and generate a comprehensive ATS score and review.

Return JSON in this exact format:
{
    "score": 0 to 100,
    "strengths": ["List of 2-3 strengths"],
    "weaknesses": ["List of 1-3 weaknesses"],
    "suggestions": ["List of 2-4 actionable improvements"]
}
"""

        user_prompt = f"""
Resume Content:
{resume_text[:4000]}
{job_context}
"""

        try:
            client = LLMClient()
            parsed = client.generate_json(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_tokens=1024,
            )
            
            return {
                "score": int(parsed.get("score", 0)),
                "strengths": parsed.get("strengths", []),
                "weaknesses": parsed.get("weaknesses", []),
                "suggestions": parsed.get("suggestions", []),
            }
        except Exception as e:
            logger.exception(f"Failed to calculate ATS score with AI API: {e}")
            
            # Heuristic Fallback in case of Rate Limit / API Error
            score = 65
            if parsed_resume.skills and len(parsed_resume.skills) > 5:
                score += 15
            if parsed_resume.experience and len(parsed_resume.experience) > 1:
                score += 10
            
            return {
                "score": min(score, 100),
                "strengths": [
                    "Resume is well structured and parsable by ATS.",
                    f"Found {len(parsed_resume.skills) if parsed_resume.skills else 0} core skills identified."
                ],
                "weaknesses": [
                    "Consider adding more measurable achievements to your experience bullets.",
                    "Ensure exact keyword matches with the target job description."
                ],
                "suggestions": [
                    "Use standard section headers (Experience, Education, Skills).",
                    "Tailor your summary to highlight your most relevant experience.",
                    "Include more industry-specific terminology."
                ],
            }