from fastapi import APIRouter
import sqlite3
from fastapi import Query
from app.services.search import search_jobs

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