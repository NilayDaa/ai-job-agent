from apscheduler.schedulers.blocking import BlockingScheduler

from app.services.queue import job_queue
from app.jobs.scraper_jobs import scrape_jobs_background
from app.services.queue import redis_conn

scheduler = BlockingScheduler()

@scheduler.scheduled_job(
    "interval",
    hours=6
)
def scheduled_scrape():

    print("Scheduling scrape job...")

    if redis_conn.get("scraper_running"):
        print("Scraper already running.")
        return

    redis_conn.set(
        "scraper_running",
        "1"
    )

    job_queue.enqueue(scrape_jobs_background)

    print("Job queued.")


if __name__ == "__main__":
    print("Scheduler started...")
    scheduler.start()