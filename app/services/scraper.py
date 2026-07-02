import json
from playwright.sync_api import sync_playwright
from app.core.database import get_connection, init_db


SEARCH_URL = "https://duunitori.fi/tyopaikat?haku=siivooja"


def scrape_jobs(max_pages=2):
    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for i in range(max_pages):
            url = f"{SEARCH_URL}&sivu={i+1}"
            print(f"Scraping: {url}")

            page.goto(url, timeout=60000)

            # IMPORTANT: wait for JS rendering
            page.wait_for_timeout(5000)

            print("Page title:", page.title())

            # 🔥 NEW APPROACH: grab all links from page
            links = page.eval_on_selector_all(
                "a",
                "elements => elements.map(e => ({text: e.innerText, href: e.href}))"
            )

            page_jobs = 0

            for l in links:
                text = l.get("text", "").strip()
                href = l.get("href", "")

                # filter job-like links
                if "/tyopaikat/" in href and len(text) > 10:
                    jobs.append({
                        "title": text,
                        "company": "Unknown",
                        "location": "Unknown",
                        "link": href
                    })
                    page_jobs += 1

            print(f"Found jobs this page: {page_jobs}")

        browser.close()

    return jobs



def save_jobs_json(jobs):
    with open("data/jobs.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    init_db()

    jobs = scrape_jobs()

    save_jobs_json(jobs)
    save_jobs_to_db(jobs)

    print(f"Scraped total: {len(jobs)} jobs")