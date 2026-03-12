import json
from typing import Dict, Any, List, Optional, TypedDict

from langgraph.graph import StateGraph, END

from agent.tools import (
    cv_analysis_tool,
    github_analysis_tool,
    skill_gap_tool,
    retrieve_career_knowledge
)

from agent.prompts import CAREER_ANALYSIS_PROMPT

from openai import OpenAI
from config import settings


# Initialize OpenAI
client = OpenAI(api_key=settings.OPENAI_API_KEY)


# ---------------------------------------------------
# Typed State (ensures all keys persist across nodes)
# ---------------------------------------------------

class AgentState(TypedDict, total=False):
    cv_text: str
    github_url: Optional[str]
    experience_level: str
    target_roles: list
    cv_analysis: dict
    github_analysis: dict
    skill_gap_analysis: dict
    retrieved_context: list
    career_strategy: str
    scores: dict


# ---------------------------------------------------
# Score Computation Node
# ---------------------------------------------------

def compute_scores_node(state: dict) -> dict:
    """
    Compute numerical scores for frontend charts from all collected data.
    """

    cv_data = state.get("cv_analysis", {})
    github_data = state.get("github_analysis", {})
    skill_gap = state.get("skill_gap_analysis", {})
    experience_level = state.get("experience_level", "Not specified")
    target_roles = state.get("target_roles", [])

    skills = cv_data.get("skills", [])
    projects = cv_data.get("projects", [])
    experience_years = cv_data.get("experience_years", 0)

    # Technical skills score (based on # of skills extracted)
    technical_score = min(len(skills) * 8, 100)

    # Projects score
    projects_score = min(len(projects) * 20, 100)

    # Experience score
    exp_map = {
        "fresher": 10, "1 year": 20, "2 years": 35, "3 years": 50,
        "4 years": 60, "5+ years": 75, "7+ years": 85, "10+ years": 95
    }
    experience_score = exp_map.get(experience_level.lower(), min(experience_years * 10, 100))

    # GitHub score
    repo_count = github_data.get("repo_count", 0)
    portfolio_score_raw = github_data.get("portfolio_score", 0)
    github_score = min(int(portfolio_score_raw), 100) if portfolio_score_raw else min(repo_count * 5, 100)

    # Role fit score (based on skill overlap with target roles)
    current_skills = set(s.lower() for s in skills)
    role_keywords = set()
    for role in target_roles:
        for word in role.lower().split():
            role_keywords.add(word)
    
    if role_keywords:
        overlap = len(current_skills.intersection(role_keywords))
        role_fit_score = min(overlap * 25, 100) if overlap else 30
    else:
        role_fit_score = 50  # neutral if no roles specified

    # Skills matched vs missing
    skills_matched = len(skill_gap.get("current_skills", []))
    skills_missing = len(skill_gap.get("missing_skills", []))

    # Overall score (weighted average)
    overall = int(
        0.30 * technical_score +
        0.20 * experience_score +
        0.20 * projects_score +
        0.15 * github_score +
        0.15 * role_fit_score
    )

    scores = {
        "overall": overall,
        "technical_skills": technical_score,
        "projects": projects_score,
        "experience": experience_score,
        "github": github_score,
        "role_fit": role_fit_score,
        "skills_matched": skills_matched,
        "skills_missing": skills_missing,
        "experience_level": experience_level,
        "target_roles_count": len(target_roles),
        "repo_count": repo_count,
        "portfolio_score": portfolio_score_raw,
    }

    return {"scores": scores}


# ---------------------------------------------------
# Reasoning Node
# ---------------------------------------------------

def reasoning_node(state: dict) -> dict:
    """
    Final reasoning step using LLM
    Combines all agent outputs into a career strategy
    """

    cv_data = state.get("cv_analysis", {})
    github_data = state.get("github_analysis", {})
    skill_gap = state.get("skill_gap_analysis", {})
    retrieved = state.get("retrieved_context", [])
    experience_level = state.get("experience_level", "Not specified")
    target_roles = state.get("target_roles", [])

    prompt = CAREER_ANALYSIS_PROMPT.format(
        skills=cv_data.get("skills", []),
        projects=cv_data.get("projects", []),
        experience_years=cv_data.get("experience_years", 0),
        experience_level=experience_level,
        target_roles=", ".join(target_roles) if target_roles else "Not specified",

        repo_count=github_data.get("repo_count", 0),
        top_languages=github_data.get("top_languages", []),
        total_stars=github_data.get("total_stars", 0),
        portfolio_score=github_data.get("portfolio_score", 0),

        current_skills=skill_gap.get("current_skills", []),
        missing_skills=skill_gap.get("missing_skills", []),

        retrieved_context="\n".join(retrieved) if retrieved else "No additional context available."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    result = response.choices[0].message.content.strip()

    if result.startswith("```markdown"):
        result = result[11:].strip()
    elif result.startswith("```"):
        result = result[3:].strip()
        
    if result.endswith("```"):
        result = result[:-3].strip()

    return {
        "career_strategy": result
    }


# ---------------------------------------------------
# Build LangGraph Agent
# ---------------------------------------------------

def build_agent():

    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("cv_analysis", cv_analysis_tool)
    workflow.add_node("github_analysis", github_analysis_tool)
    workflow.add_node("skill_gap", skill_gap_tool)
    workflow.add_node("knowledge_retrieval", retrieve_career_knowledge)
    workflow.add_node("compute_scores", compute_scores_node)
    workflow.add_node("reasoning", reasoning_node)

    # Entry point
    workflow.set_entry_point("cv_analysis")

    # Define pipeline
    workflow.add_edge("cv_analysis", "github_analysis")
    workflow.add_edge("github_analysis", "skill_gap")
    workflow.add_edge("skill_gap", "knowledge_retrieval")
    workflow.add_edge("knowledge_retrieval", "compute_scores")
    workflow.add_edge("compute_scores", "reasoning")

    # End
    workflow.add_edge("reasoning", END)

    return workflow.compile()


# ---------------------------------------------------
# Agent instance
# ---------------------------------------------------

career_agent = build_agent()