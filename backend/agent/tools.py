from typing import Dict, Any

from services.cv_parser import CVParser
from services.github_parser import GithubParser
from services.vector_store import VectorStore


# Initialize shared services
cv_parser = CVParser()
github_parser = GithubParser()
vector_store = VectorStore()


# ---------------------------------------------------
# CV Analysis Tool
# ---------------------------------------------------

def cv_analysis_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract skills, projects, and experience from CV
    """

    cv_text = state.get("cv_text")

    if not cv_text:
        return {"cv_analysis": {}}

    result = cv_parser.analyze(cv_text)

    return {
        "cv_analysis": result
    }


# ---------------------------------------------------
# GitHub Portfolio Analysis Tool
# ---------------------------------------------------

def github_analysis_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze GitHub repositories
    """

    github_url = state.get("github_url")

    if not github_url:
        return {"github_analysis": {}}

    # Ensure it's a string (could be a Pydantic Url object)
    github_url = str(github_url)

    result = github_parser.analyze(github_url)

    return {
        "github_analysis": result
    }


# ---------------------------------------------------
# Skill Gap Detection Tool
# ---------------------------------------------------

def skill_gap_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compare candidate skills with industry expectations
    """

    cv_data = state.get("cv_analysis", {})

    skills = cv_data.get("skills", [])

    # Example industry skill expectations
    backend_stack = {
        "python",
        "docker",
        "kubernetes",
        "system design",
        "postgresql",
        "redis"
    }

    current_skills = set([s.lower() for s in skills])

    missing = backend_stack - current_skills

    return {
        "skill_gap_analysis": {
            "current_skills": list(current_skills),
            "missing_skills": list(missing),
            "recommended_skills": list(missing)
        }
    }


# ---------------------------------------------------
# Vector Knowledge Retrieval Tool
# ---------------------------------------------------

def retrieve_career_knowledge(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retrieve relevant career knowledge from Qdrant
    """

    cv_data = state.get("cv_analysis", {})
    github_data = state.get("github_analysis", {})

    skills = cv_data.get("skills", [])

    query = "career advice for " + ", ".join(skills)

    docs = vector_store.search(query)

    return {
        "retrieved_context": docs
    }