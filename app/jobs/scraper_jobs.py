from app.repositories.jobs_repository import save_jobs
from app.services.scraper import scrape_jobs
from app.services.semantic_search import semantic_search


def scrape_jobs_background():

    print("=" * 60)
    print("Background scraping started")
    print("=" * 60)

    jobs = scrape_jobs(max_pages=2)

    inserted = save_jobs(jobs)

    print(f"Inserted {inserted} jobs")

    # Rebuild vector index
    semantic_search.vector_store.build_index(jobs)
    semantic_search.vector_store.save()

    print("Vector index rebuilt")

    print("=" * 60)
    print("Background scraping finished")
    print("=" * 60)