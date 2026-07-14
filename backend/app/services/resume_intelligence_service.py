import re


class ResumeIntelligenceService:

    @staticmethod
    def extract_skills(skill_lines: list[str]) -> dict:

        categories = {
            "languages": [],
            "frameworks": [],
            "ai_ml": [],
            "databases": [],
            "cloud": [],
            "tools": [],
            "other": [],
        }

        mapping = {
            "languages": [
                "python",
                "java",
                "javascript",
                "typescript",
                "sql",
                "c",
                "c++",
                "c#",
                "go",
                "rust",
            ],
            "frameworks": [
                "fastapi",
                "flask",
                "django",
                "langchain",
                "langgraph",
                "llamaindex",
                "tensorflow",
                "pytorch",
                "hugging face",
                "react",
                "node",
            ],
            "ai_ml": [
                "machine learning",
                "deep learning",
                "nlp",
                "rag",
                "llm",
                "openai",
                "claude",
                "gemini",
                "mistral",
                "bert",
                "transformers",
                "embeddings",
                "faiss",
                "prompt engineering",
            ],
            "databases": [
                "postgresql",
                "mysql",
                "sqlite",
                "mongodb",
                "redis",
            ],
            "cloud": [
                "aws",
                "azure",
                "gcp",
                "google cloud",
            ],
            "tools": [
                "git",
                "docker",
                "kubernetes",
                "jira",
                "ci/cd",
                "postman",
                "linux",
                "github",
            ],
        }

        text = " ".join(skill_lines)

        skills = [
            skill.strip()
            for skill in re.split(r",|:", text)
            if skill.strip()
        ]

        for skill in skills:

            lower = skill.lower()

            found = False

            for category, keywords in mapping.items():

                for keyword in keywords:

                    if keyword in lower:

                        if skill not in categories[category]:
                            categories[category].append(skill)

                        found = True
                        break

                if found:
                    break

            if not found:
                categories["other"].append(skill)

        return categories