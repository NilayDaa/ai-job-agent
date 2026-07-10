from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import init_db


# IMPORTANT:
# Create database tables before importing routers
init_db()


from app.api.jobs import router as jobs_router
from app.api import cv
from app.api import auth


app = FastAPI()


app.include_router(cv.router)

app.include_router(auth.router)

app.include_router(jobs_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        # add your Vercel URL later
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "AI Job Agent running"
    }