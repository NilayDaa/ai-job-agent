import os

from fastapi import APIRouter, UploadFile, File

from app.services.cv_parser import cv_parser
from app.services.skill_extractor import extract_skills
from app.agents.job_agent import job_agent
from fastapi import Depends
from app.core.security import get_current_user
from app.repositories.cv_repository import save_user_cv
from app.repositories.cv_repository import get_user_cv

router = APIRouter()


@router.post("/match-cv")
async def match_cv(file: UploadFile = File(...), current_user=Depends(get_current_user)):

    filepath = f"uploads/{file.filename}"

    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())
        save_user_cv(
            user_id=current_user["id"],
            filename=file.filename,
            filepath=filepath
        )

    # Extract CV text
    cv_text = cv_parser.extract_text(filepath)

    # Extract skills
    skills = extract_skills(cv_text)

    # Match CV against jobs using the AI Agent
    jobs = job_agent.match_cv(cv_text)

    # Generate AI career analysis
    analysis = job_agent.analyze(
        cv_text=cv_text,
        skills=skills,
        jobs=jobs
    )

    # Remove uploaded file
    if os.path.exists(filepath):
        os.remove(filepath)

    return {
        "cv_summary": {
            "characters": len(cv_text),
            "skills_found": skills,
            "top_matches": len(jobs)
        },
        "recommendations": jobs,
        "career_analysis": analysis
    }

@router.get("/my-cv")
def my_cv(current_user=Depends(get_current_user)):

    cv = get_user_cv(current_user["id"])

    if cv is None:
        return {
            "message": "No CV uploaded yet"
        }

    return cv