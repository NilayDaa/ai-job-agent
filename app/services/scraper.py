import json

from playwright.sync_api import sync_playwright

from app.core.database import init_db
from app.repositories.jobs_repository import save_jobs
from app.config import SEARCH_TERMS
from app.services.vector_store import VectorStore
from app.repositories.jobs_repository import get_all_jobs
from app.services.semantic_search import semantic_search
from app.services.cache import cache


BASE_URL = "https://duunitori.fi/tyopaikat"


def scrape_jobs(max_pages=2):

    jobs = {}

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        for term in SEARCH_TERMS:

            print("\n" + "=" * 60)
            print(f"Searching: {term}")
            print("=" * 60)

            for page_number in range(1, max_pages + 1):

                search_url = (
                    f"{BASE_URL}"
                    f"?haku={term}"
                    f"&sivu={page_number}"
                )

                print("Scraping:", search_url)

                try:

                    page.goto(
                        search_url,
                        timeout=60000,
                        wait_until="domcontentloaded"
                    )

                    page.wait_for_timeout(3000)

                    print("Page title:", page.title())

                    cards = page.locator("div.job-box")

                    page_jobs = 0

                    for i in range(cards.count()):

                        try:

                            card = cards.nth(i)

                            link = card.locator(
                                "a.job-box__hover.gtm-search-result"
                            ).first

                            if link.count() == 0:
                                continue

                            title = link.inner_text().strip()

                            href = link.get_attribute("href") or ""

                            if not href:
                                continue

                            if href.startswith("/"):
                                href = "https://duunitori.fi" + href

                            company = (
                                link.get_attribute("data-company")
                                or "Unknown"
                            ).strip()

                            try:
                                location = (
                                    card
                                    .locator("span.job-box__job-location")
                                    .inner_text()
                                    .strip()
                                )
                            except:
                                location = "Unknown"

                            if href in jobs:
                                continue

                            jobs[href] = {
                                "title": title,
                                "company": company,
                                "location": location,
                                "link": href,
                                "search_term": term,
                            }

                            print(f"Found: {title}")

                            page_jobs += 1

                        except Exception as e:
                            print("Card error:", e)

                    print(f"Found jobs this page: {page_jobs}")

                except Exception as e:

                    print("Search error:", e)

        browser.close()

    print(f"\nUnique jobs collected: {len(jobs)}")

    return list(jobs.values())


def save_jobs_json(jobs):

    with open(
        "data/jobs.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            jobs,
            f,
            indent=4,
            ensure_ascii=False
        )


def main():

    init_db()

    jobs = scrape_jobs(max_pages=2)

    save_jobs_json(jobs)

    inserted = save_jobs(jobs)
    rows = get_all_jobs()

    all_jobs = []

    for row in rows:
        all_jobs.append(
            {
                "id": row[0],
                "title": row[1],
                "company": row[2],
                "location": row[3],
                "link": row[4],
            }
        )

    VectorStore().rebuild(all_jobs)
    cache.flushdb()

    semantic_search.reload()

    print(f"\nScraped: {len(jobs)} jobs")
    print(f"Inserted: {inserted} new jobs")


if __name__ == "__main__":
    main()