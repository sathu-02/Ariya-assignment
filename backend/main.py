import json
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from models.schemas import CareerAnalysisResponse
from agent.graph import career_agent
from utils.file_parser import parse_file_content


# ---------------------------------------------------
# FastAPI App Initialization
# ---------------------------------------------------

app = FastAPI(
    title="Career Portfolio Intelligence Agent",
    description="AI agent that analyzes CVs and GitHub portfolios to generate career improvement strategies",
    version="1.0.0"
)


# ---------------------------------------------------
# CORS Configuration (needed for React frontend)
# ---------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------
# Health Check Endpoint
# ---------------------------------------------------

@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "Career Portfolio Intelligence Agent"
    }


# ---------------------------------------------------
# Main Agent Endpoint
# ---------------------------------------------------

@app.post("/analyze")
async def analyze_portfolio(
    resume: Optional[UploadFile] = File(None),
    cv_text: Optional[str] = Form(None),
    github_url: Optional[str] = Form(None),
    experience_level: Optional[str] = Form(None),
    target_roles: Optional[str] = Form(None),
):

    try:

        final_cv_text = ""
        
        # Parse directly from uploaded file if provided
        if resume:
            file_bytes = await resume.read()
            final_cv_text = parse_file_content(resume.filename, file_bytes)
            
        # Fallback to pasted text
        if not final_cv_text and cv_text:
            final_cv_text = cv_text
            
        if not final_cv_text:
            raise HTTPException(status_code=400, detail="No CV content could be extracted or provided.")

        # Parse target_roles from JSON string
        parsed_roles = []
        if target_roles:
            try:
                parsed_roles = json.loads(target_roles)
            except Exception:
                parsed_roles = [target_roles]

        # Prepare initial state for LangGraph
        state = {
            "cv_text": final_cv_text,
            "github_url": github_url,
            "experience_level": experience_level or "Not specified",
            "target_roles": parsed_roles,
        }

        # Run agent pipeline
        result = career_agent.invoke(state)

        strategy_text = result.get("career_strategy", "")
        scores = result.get("scores", {})

        # Return response with scores
        return {
            "career_strategy": strategy_text,
            "scores": scores,
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Agent processing failed: {str(e)}"
        )