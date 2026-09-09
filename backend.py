from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from career_graph import career_graph


# --------------------------------------------------
# Create FastAPI application
# --------------------------------------------------

app = FastAPI()


# --------------------------------------------------
# CORS configuration
# Allows React frontend to communicate with FastAPI
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Request model for Skill Gap Analysis
# --------------------------------------------------

class SkillGapRequest(BaseModel):
    target_role: str
    skills: str


# --------------------------------------------------
# Skill Gap Analysis
# --------------------------------------------------

@app.post("/skill-gap")
def skill_gap(request: SkillGapRequest):

    result = career_graph.invoke({
        "question": "skill gap",
        "skills": request.skills,
        "target_role": request.target_role,
        "resume_path": "",
        "result": ""
    })

    return {
        "result": result["result"]
    }


# --------------------------------------------------
# Resume Analysis
# --------------------------------------------------

@app.post("/resume-analysis")
async def resume_analysis(
    target_role: str = Form(...),
    resume: UploadFile = File(...)
):

    # Temporary path for uploaded resume
    file_path = f"temp_{resume.filename}"

    # Save uploaded PDF
    with open(file_path, "wb") as file:
        file.write(await resume.read())

    # Run Resume Analysis through LangGraph
    result = career_graph.invoke({
        "question": "resume analysis",
        "skills": "",
        "target_role": target_role,
        "resume_path": file_path,
        "result": ""
    })

    return {
        "result": result["result"]
    }


# --------------------------------------------------
# Interview Preparation
# --------------------------------------------------

@app.post("/interview-prep")
def interview_prep(
    target_role: str = Form(...)
):

    # Run Interview Preparation through LangGraph
    result = career_graph.invoke({
        "question": "interview preparation",
        "skills": "",
        "target_role": target_role,
        "resume_path": "",
        "result": ""
    })

    return {
        "result": result["result"]
    }