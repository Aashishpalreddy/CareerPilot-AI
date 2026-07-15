import re
from html import unescape

from bs4 import BeautifulSoup


class JobParserService:

    SKILLS = [
        "Python",
        "Java",
        "JavaScript",
        "TypeScript",
        "SQL",
        "FastAPI",
        "Flask",
        "Django",
        "LangChain",
        "LangGraph",
        "LlamaIndex",
        "OpenAI",
        "OpenAI API",
        "Claude",
        "Gemini",
        "Docker",
        "Kubernetes",
        "Git",
        "GitHub",
        "PostgreSQL",
        "MySQL",
        "MongoDB",
        "Redis",
        "AWS",
        "Azure",
        "GCP",
        "TensorFlow",
        "PyTorch",
        "Scikit-learn",
        "Pandas",
        "NumPy",
        "RAG",
        "FAISS",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "REST API",
    ]


    @staticmethod
    def parse(raw_text: str):

        clean_text = JobParserService.clean_html(raw_text)

        text_lower = clean_text.lower()

        skills = [
            skill
            for skill in JobParserService.SKILLS
            if skill.lower() in text_lower
        ]


        return {
            "title": JobParserService.extract_title(clean_text),

            "company": None,

            "skills": sorted(set(skills)),

            "technologies": sorted(set(skills)),

            "experience":
                JobParserService.extract_experience(clean_text),

            "education":
                JobParserService.extract_education(clean_text),

            "responsibilities":
                JobParserService.extract_responsibilities(clean_text),

            "qualifications":
                JobParserService.extract_qualifications(clean_text),

            "keywords":
                skills,
        }


    @staticmethod
    def clean_html(text: str) -> str:

        soup = BeautifulSoup(
            text or "",
            "html.parser"
        )

        cleaned = soup.get_text("\n")

        cleaned = unescape(cleaned)

        cleaned = re.sub(
            r"\n{2,}",
            "\n",
            cleaned
        )

        return cleaned.strip()


    @staticmethod
    def extract_title(text: str):

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        if lines:
            return lines[0]

        return None


    @staticmethod
    def extract_experience(text: str):

        matches = re.findall(
            r"\d+\+?\s+years?",
            text,
            flags=re.IGNORECASE,
        )

        return list(set(matches))


    @staticmethod
    def extract_education(text: str):

        education = []

        keywords = [
            "Bachelor",
            "Master",
            "PhD",
            "Computer Science",
            "Engineering",
            "Information Technology",
        ]

        for keyword in keywords:

            if keyword.lower() in text.lower():

                education.append(keyword)

        return education


    @staticmethod
    def extract_responsibilities(text: str):

        lines = [
            line.strip()
            for line in text.splitlines()
            if len(line.strip()) > 30
        ]

        return lines[:20]


    @staticmethod
    def extract_qualifications(text: str):

        lines = [
            line.strip()
            for line in text.splitlines()
            if len(line.strip()) > 30
        ]

        return lines[:20]