import json
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright

from app.core.database import init_db
from app.repositories.jobs_repository import save_jobs
from app.services.vector_store import VectorStore
from app.repositories.jobs_repository import get_all_jobs
from app.services.semantic_search import semantic_search
from app.services.cache import cache


BASE_URL = "https://tyomarkkinatori.fi"

VACANCIES_URL = (
    "https://tyomarkkinatori.fi/en/personal-customers/vacancies"
)


def extract_vacancies(page, jobs):

    links = page.locator(
        'h3 a[href*="/en/personal-customers/vacancies/"]'
    )

    count = links.count()

    print(f"Vacancies found on page: {count}")

    page_jobs = 0

    for i in range(count):

        try:

            link = links.nth(i)

            title = link.inner_text().strip()

            href = link.get_attribute("href") or ""

            if not title or not href:
                continue

            href = urljoin(
                BASE_URL,
                href
            )

            # Avoid duplicates
            if href in jobs:
                continue

            # Find vacancy card
            card = link.locator(
                "xpath=ancestor::div[h3][1]"
            )

            if card.count() == 0:
                continue

            # -------------------------
            # COMPANY
            # -------------------------

            company = "Unknown"

            company_items = card.locator(
                "ul li"
            )

            if company_items.count() > 0:

                company = (
                    company_items
                    .nth(0)
                    .inner_text()
                    .strip()
                )

            # -------------------------
            # LOCATION
            # -------------------------

            location = "Unknown"

            location_icon = card.locator(
                'svg[data-icon="location"]'
            )

            if location_icon.count() > 0:

                try:

                    location = (
                        location_icon
                        .locator("xpath=../..")
                        .inner_text()
                        .strip()
                    )

                except Exception:
                    pass

            # -------------------------
            # SAVE
            # -------------------------

            jobs[href] = {
                "title": title,
                "company": company,
                "location": location,
                "link": href,
            }

            print(
                f"Found: {title} | "
                f"{company} | "
                f"{location}"
            )

            page_jobs += 1

        except Exception as e:

            print(
                f"Card error at index {i}: {e}"
            )

    print(
        f"New jobs collected from this page: "
        f"{page_jobs}"
    )


def scrape_jobs(max_pages=5):

    jobs = {}

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        for page_number in range(
            1,
            max_pages + 1
        ):

            print("\n" + "=" * 70)

            print(
                f"SCRAPING PAGE "
                f"{page_number}/{max_pages}"
            )

            print("=" * 70)

            # --------------------------------
            # Työmarkkinatori pagination
            # --------------------------------
            #
            # Page 1:
            # ?p=1
            #
            # Page 2:
            # ?p=2
            #
            # Page 3:
            # ?p=3
            #
            # etc.
            #
            # --------------------------------

            current_url = (
                f"{VACANCIES_URL}"
                f"?p={page_number}"
            )

            print(
                "URL:",
                current_url
            )

            response = page.goto(
                current_url,
                timeout=60000,
                wait_until="networkidle"
            )

            # --------------------------------
            # HTTP status
            # --------------------------------

            if response:

                print(
                    "HTTP:",
                    response.status
                )

                if response.status >= 400:

                    raise RuntimeError(
                        f"HTTP error: "
                        f"{response.status}"
                    )

            # --------------------------------
            # Page information
            # --------------------------------

            print(
                "TITLE:",
                page.title()
            )

            # --------------------------------
            # Wait for vacancy listings
            # --------------------------------

            page.wait_for_selector(
                'h3 a[href*="/en/personal-customers/vacancies/"]',
                timeout=30000
            )

            vacancy_count = page.locator(
                'h3 a[href*="/en/personal-customers/vacancies/"]'
            ).count()

            if vacancy_count == 0:

                print(
                    "No vacancies found. "
                    "Stopping."
                )

                break

            # --------------------------------
            # Extract jobs
            # --------------------------------

            extract_vacancies(
                page,
                jobs
            )

            print(
                f"TOTAL UNIQUE JOBS SO FAR: "
                f"{len(jobs)}"
            )

        browser.close()

    # --------------------------------
    # Final result
    # --------------------------------

    print("\n" + "=" * 70)

    print(
        f"TOTAL UNIQUE JOBS: "
        f"{len(jobs)}"
    )

    print("=" * 70)

    if not jobs:

        raise RuntimeError(
            "Työmarkkinatori scraper "
            "returned 0 jobs."
        )

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

    # --------------------------------
    # Initialize database
    # --------------------------------

    init_db()

    # --------------------------------
    # Scrape 5 pages
    # --------------------------------

    jobs = scrape_jobs(
        max_pages=5
    )

    # --------------------------------
    # Save JSON
    # --------------------------------

    save_jobs_json(
        jobs
    )

    # --------------------------------
    # Save to PostgreSQL
    # --------------------------------

    inserted = save_jobs(
        jobs
    )

    # --------------------------------
    # Get ALL jobs from database
    # --------------------------------

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

    # --------------------------------
    # Rebuild vector index
    # --------------------------------

    VectorStore().rebuild(
        all_jobs
    )

    # --------------------------------
    # Clear Redis cache
    # --------------------------------

    cache.flushdb()

    # --------------------------------
    # Reload semantic search
    # --------------------------------

    semantic_search.reload()

    # --------------------------------
    # Final statistics
    # --------------------------------

    print(
        f"\nScraped: "
        f"{len(jobs)} jobs"
    )

    print(
        f"Inserted: "
        f"{inserted} new jobs"
    )


if __name__ == "__main__":
    main()