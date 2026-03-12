import json
import re
from typing import Dict, Any

from openai import OpenAI
from config import settings


class CVParser:
    """
    Intelligent CV parser using LLM-based extraction.

    Extracts:
    - skills
    - projects
    - domains
    - estimated experience
    """

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    # ---------------------------------------------------
    # Text Cleaning
    # ---------------------------------------------------

    def clean_text(self, text: str) -> str:
        """
        Normalize CV text for analysis
        """

        text = text.replace("\n", " ")
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # ---------------------------------------------------
    # LLM Skill + Project Extraction
    # ---------------------------------------------------

    def llm_extract(self, cv_text: str) -> Dict[str, Any]:
        """
        Use OpenAI to extract structured CV information
        """

        prompt = f"""
You are an AI resume analyzer.

Extract structured information from the following CV.

Return STRICT JSON with this format:

{{
 "skills": [],
 "projects": [],
 "domains": [],
 "experience_years": number
}}

Rules:
- Skills should include programming languages, frameworks, tools, and technologies.
- Projects should be meaningful project names mentioned.
- Domains include fields like AI, Backend Engineering, Data Science etc.
- Estimate experience_years from CV context.

CV:
{cv_text}
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except Exception:
            return self.fallback_parse(cv_text)

    # ---------------------------------------------------
    # Fallback Parsing (if LLM fails)
    # ---------------------------------------------------

    def fallback_parse(self, cv_text: str) -> Dict[str, Any]:
        """
        Basic heuristic parsing when LLM fails
        """

        text = self.clean_text(cv_text).lower()

        experience_patterns = [
            r"(\d+)\+?\s+years",
            r"(\d+)\s+yrs"
        ]

        years = []

        for pattern in experience_patterns:
            matches = re.findall(pattern, text)
            for m in matches:
                years.append(int(m))

        experience = max(years) if years else 0

        return {
            "skills": [],
            "projects": [],
            "domains": [],
            "experience_years": experience
        }

    # ---------------------------------------------------
    # Main Analysis Pipeline
    # ---------------------------------------------------

    def analyze(self, cv_text: str) -> Dict[str, Any]:
        """
        Full CV analysis pipeline
        """

        cv_text = self.clean_text(cv_text)

        extracted = self.llm_extract(cv_text)

        return {
            "skills": extracted.get("skills", []),
            "projects": extracted.get("projects", []),
            "domains": extracted.get("domains", []),
            "experience_years": extracted.get("experience_years", 0)
        }