import json
from playwright.sync_api import sync_playwright


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

            # IMPORTANT: wait for network + content
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)

            # DEBUG: check if page has content
            print("Page title:", page.title())

            # More generic selector (safer)
            cards = page.locator("a[href*='/tyopaikat/']")

            count = cards.count()
            print(f"Found links: {count}")

            for j in range(count):
                el = cards.nth(j)

                title = safe_text(el)
                link = el.get_attribute("href")

                if title and link:
                    jobs.append({
                        "title": title,
                        "link": f"https://duunitori.fi{link}" if link.startswith("/") else link
                    })

        browser.close()

    return jobs


def safe_text(element):
    try:
        return element.inner_text().strip()
    except:
        return None


def save_jobs(jobs):
    with open("data/jobs.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    jobs = scrape_jobs()
    save_jobs(jobs)
    print(f"Scraped {len(jobs)} jobs from Duunitori")