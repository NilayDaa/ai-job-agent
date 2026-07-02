from app.core.database import init_db
from app.repositories.jobs_repository import save_jobs
from app.services.scraper import scrape_jobs, save_jobs_json


def main():
    init_db()

    jobs = scrape_jobs()

    save_jobs_json(jobs)

    inserted = save_jobs(jobs)

    print(f"Scraped: {len(jobs)} jobs")
    print(f"Inserted: {inserted} new jobs")


if __name__ == "__main__":
    main()