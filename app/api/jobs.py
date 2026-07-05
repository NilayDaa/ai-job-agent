from fastapi import APIRouter, Query

from app.services.search import search_jobs
from app.agents.job_agent import job_agent
from app.repositories.jobs_repository import get_all_jobs

router = APIRouter()


@router.get("/jobs")
def get_jobs():

    rows = get_all_jobs()

    return [
        {
            "title": r[1],
            "company": r[2],
            "location": r[3],
            "link": r[4]
        }
        for r in rows
    ]


# Optional: Keep keyword search for comparison
@router.get("/search")
def keyword_search(query: str = Query(...)):
    return search_jobs(query)


# Main AI-powered semantic search
@router.get("/semantic-search")
def semantic_search(query: str = Query(...), k: int = 10):
    return job_agent.search_jobs(query, k)