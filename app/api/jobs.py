from fastapi import APIRouter
import sqlite3
from fastapi import Query
from app.services.search import search_jobs
from app.services.semantic_search import semantic_search
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

@router.get("/search")
def search(query: str = Query(...)):
    return search_jobs(query)

@router.get("/semantic-search")
def semantic_search_endpoint(
    q: str = Query(..., description="Search query"),
    k: int = 10
):
    return semantic_search.search(q, k)

@router.get("/agent-search")
def agent_search(query: str = Query(...)):
    return job_agent.search_jobs(query)