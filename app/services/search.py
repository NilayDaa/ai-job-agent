from app.core.database import get_connection


def search_jobs(query: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title, company, location, link
        FROM jobs
    """)

    rows = cursor.fetchall()
    conn.close()

    query = query.lower()

    results = []

    for row in rows:
        title, company, location, link = row

        score = 0

        if title and query in title.lower():
            score += 10

        if company and query in company.lower():
            score += 5

        if location and query in location.lower():
            score += 3

        if score > 0:
            results.append({
                "title": title,
                "company": company,
                "location": location,
                "link": link,
                "score": score
            })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results