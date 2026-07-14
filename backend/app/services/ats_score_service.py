class ATSScoreService:

    @staticmethod
    def calculate(parsed_resume):

        score = 100

        strengths = []
        weaknesses = []
        suggestions = []

        # Skills
        if parsed_resume.skills:
            strengths.append("Technical skills detected.")
        else:
            score -= 20
            weaknesses.append("No technical skills found.")
            suggestions.append("Add a dedicated Skills section.")

        # Experience
        if parsed_resume.experience:
            strengths.append("Professional experience detected.")
        else:
            score -= 25
            weaknesses.append("No work experience found.")
            suggestions.append("Add professional experience.")

        # Education
        if parsed_resume.education:
            strengths.append("Education section detected.")
        else:
            score -= 10
            weaknesses.append("Education section missing.")
            suggestions.append("Add education details.")

        # Projects
        if parsed_resume.projects:
            strengths.append("Projects section detected.")
        else:
            score -= 10
            weaknesses.append("Projects missing.")
            suggestions.append("Add projects.")

        # Certifications
        if parsed_resume.certifications:
            strengths.append("Certifications detected.")

        return {
            "score": max(score, 0),
            "strengths": strengths,
            "weaknesses": weaknesses,
            "suggestions": suggestions,
        }