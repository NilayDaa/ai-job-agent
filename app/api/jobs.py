from fastapi import APIRouter, Query
import sqlite3

from app.services.search import search_jobs
from app.agents.job_agent import job_agent

router = APIRouter()

DB_PATH = "data/jobs.db"


@router.get("/jobs")
def get_jobs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT title, company, location, link FROM jobs")
    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "title": r[0],
            "company": r[1],
            "location": r[2],
            "link": r[3]
        }
        for r in rows
    ]


# Optional: Keep keyword search for comparison
@router.get("/search")
def keyword_search(query: str = Query(...)):
    return search_jobs(query)


# Main search endpoint (uses the AI Agent)
@router.get("/semantic-search")
def semantic_search(query: str = Query(...), k: int = 10):
    return job_agent.search_jobs(query, k)