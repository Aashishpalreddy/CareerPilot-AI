import re


class ResumeSectionExtractor:

    SECTION_HEADERS = {
        "skills": [
            "technical skills",
            "skills",
            "core competencies",
        ],
        "experience": [
            "professional experience",
            "work experience",
            "experience",
        ],
        "education": [
            "education",
        ],
        "projects": [
            "projects",
            "academic projects",
            "personal projects",
        ],
        "certifications": [
            "certifications",
            "certifications & training",
            "training",
            "licenses",
        ],
    }

    @classmethod
    def extract_sections(cls, text: str) -> dict:

        sections = {
            "skills": [],
            "experience": [],
            "education": [],
            "projects": [],
            "certifications": [],
        }

        current_section = None

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        for line in lines:

            normalized = re.sub(
                r"\s+",
                " ",
                line.lower().strip(),
            )

            matched = False

            for section, headers in cls.SECTION_HEADERS.items():

                if any(header in normalized for header in headers):
                    current_section = section
                    matched = True
                    break

            if matched:
                continue

            if current_section:
                sections[current_section].append(line)

        return sections