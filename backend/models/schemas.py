from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional


# -----------------------------
# Request Schema
# -----------------------------

class AnalyzeRequest(BaseModel):
    """
    Request payload for portfolio analysis
    """
    cv_text: str = Field(
        ...,
        description="Raw CV text extracted from uploaded resume"
    )

    github_url: Optional[HttpUrl] = Field(
        None,
        description="GitHub profile URL of the candidate"
    )


# -----------------------------
# GitHub Repository Model
# -----------------------------

class Repository(BaseModel):
    """
    Represents a GitHub repository analyzed by the agent
    """
    name: str
    url: HttpUrl
    language: Optional[str]
    stars: int
    forks: Optional[int] = 0
    description: Optional[str] = None


# -----------------------------
# CV Analysis Result
# -----------------------------

class CVAnalysis(BaseModel):
    """
    Parsed insights from CV
    """
    extracted_skills: List[str] = []
    detected_projects: List[str] = []
    experience_years: Optional[int] = None


# -----------------------------
# GitHub Analysis Result
# -----------------------------

class GithubAnalysis(BaseModel):
    """
    Parsed GitHub portfolio insights
    """
    repositories: List[Repository] = []
    top_languages: List[str] = []
    total_stars: int = 0
    repo_count: int = 0


# -----------------------------
# Skill Gap Detection
# -----------------------------

class SkillGapAnalysis(BaseModel):
    """
    Comparison between candidate skills and market demands
    """
    current_skills: List[str]
    missing_skills: List[str]
    recommended_skills: List[str]


# -----------------------------
# Agent State (LangGraph)
# -----------------------------

class AgentState(BaseModel):
    """
    Shared state across LangGraph nodes
    """

    cv_text: str
    github_url: Optional[str]

    cv_analysis: Optional[CVAnalysis] = None
    github_analysis: Optional[GithubAnalysis] = None
    skill_gap_analysis: Optional[SkillGapAnalysis] = None

    career_strategy: Optional[str] = None


# -----------------------------
# Final API Response
# -----------------------------

class CareerAnalysisResponse(BaseModel):
    """
    Final response returned to frontend
    """

    career_readiness_score: Optional[int] = Field(
        None,
        description="AI estimated career readiness score"
    )

    key_strengths: List[str] = []

    weaknesses: List[str] = []

    skill_gaps: List[str] = []

    recommended_skills: List[str] = []

    suggested_projects: List[str] = []

    career_strategy: str