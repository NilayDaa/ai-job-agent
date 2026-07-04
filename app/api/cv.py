import os

from fastapi import APIRouter, UploadFile, File

from app.services.cv_parser import cv_parser
from app.services.cv_matcher import cv_matcher

router = APIRouter()


@router.post("/match-cv")
async def match_cv(file: UploadFile = File(...)):

    filepath = f"uploads/{file.filename}"

    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    cv_text = cv_parser.extract_text(filepath)

    jobs = cv_matcher.match(cv_text)

    os.remove(filepath)

    return jobs