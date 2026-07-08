from app.repositories.jobs_repository import save_jobs
from app.services.scraper import scrape_jobs
from app.services.semantic_search import semantic_search
from app.services.queue import redis_conn
import time
from app.core.logger import logger


def scrape_jobs_background():

    try:

        for attempt in range(1, 4):

            try:

                logger.info(f"Scraping attempt {attempt}")

                jobs = scrape_jobs(max_pages=2)

                inserted = save_jobs(jobs)

                semantic_search.vector_store.build_index(jobs)
                semantic_search.vector_store.save()

                logger.info(f"{inserted} jobs saved.")

                # Success → stop retrying
                break

            except Exception as e:

                logger.info(f"Scraping failed: {e}")

                if attempt == 3:
                    logger.info("Maximum retries reached.")
                    raise

                logger.info("Retrying in 10 seconds...")
                time.sleep(10)

    finally:

        redis_conn.delete("scraper_running")

        logger.info("Scraper lock released.")