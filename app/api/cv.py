import os

from fastapi import APIRouter, UploadFile, File

from app.services.cv_parser import cv_parser
from app.services.cv_matcher import cv_matcher
from app.services.skill_extractor import extract_skills
from app.services.career_analyzer import career_analyzer

router = APIRouter()


@router.post("/match-cv")
async def match_cv(file: UploadFile = File(...)):

    filepath = f"uploads/{file.filename}"

    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    # Extract CV text
    cv_text = cv_parser.extract_text(filepath)

    # Extract skills
    skills = extract_skills(cv_text)

    # Find matching jobs
    jobs = cv_matcher.match(cv_text)

    # AI career analysis
    analysis = career_analyzer.analyze(
        cv_text=cv_text,
        skills=skills,
        jobs=jobs
    )

    # Delete uploaded file
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
