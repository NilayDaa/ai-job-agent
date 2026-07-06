from fastapi import FastAPI
from app.api.jobs import router as jobs_router
from app.api import cv
from app.api import auth



app = FastAPI()

app.include_router(cv.router)

app.include_router(auth.router)

app.include_router(jobs_router)


@app.get("/")
def home():
    return {"message": "AI Job Agent running"}