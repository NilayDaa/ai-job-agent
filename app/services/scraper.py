import json
from playwright.sync_api import sync_playwright

from app.config import SEARCH_TERMS

BASE_URL = "https://duunitori.fi/tyopaikat"


def scrape_jobs(max_pages=2):
    """
    Scrape jobs from multiple search terms.
    Duplicate jobs are removed using the job URL.
    """

    jobs = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for term in SEARCH_TERMS:

            print("\n" + "=" * 60)
            print(f"Searching: {term}")
            print("=" * 60)

            for page_number in range(1, max_pages + 1):

                url = f"{BASE_URL}?haku={term}&sivu={page_number}"

                print(f"Scraping: {url}")

                try:
                    page.goto(url, timeout=60000)

                    page.wait_for_load_state("networkidle")
                    page.wait_for_timeout(3000)

                    print("Page title:", page.title())

                    links = page.eval_on_selector_all(
                        "a",
                        """
                        elements => elements.map(e => ({
                            text: e.innerText,
                            href: e.href
                        }))
                        """
                    )

                    page_jobs = 0

                    for link in links:

                        title = link.get("text", "").strip()
                        href = link.get("href", "").strip()

                        if not href:
                            continue

                        if "/tyopaikat/" not in href:
                            continue

                        if len(title) < 5:
                            continue

                        jobs[href] = {
                            "title": title,
                            "company": "Unknown",
                            "location": "Unknown",
                            "link": href,
                            "search_term": term,
                        }

                        page_jobs += 1

                    print(f"Found jobs this page: {page_jobs}")

                except Exception as e:
                    print(f"Error scraping {url}")
                    print(e)

        browser.close()

    print(f"\nUnique jobs collected: {len(jobs)}")

    return list(jobs.values())


def save_jobs_json(jobs):
    with open("data/jobs.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=4, ensure_ascii=False)