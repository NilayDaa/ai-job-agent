from app.core.database import get_connection


def save_jobs(jobs):
    conn = get_connection()
    cursor = conn.cursor()

    inserted = 0

    for job in jobs:
        try:
            cursor.execute("""
                INSERT INTO jobs
                (title, company, location, link)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (link) DO NOTHING
            """, (
                job.get("title"),
                job.get("company", "Unknown"),
                job.get("location", "Unknown"),
                job.get("link")
            ))

            if cursor.rowcount > 0:
                inserted += 1

        except Exception as e:
            print(e)

    conn.commit()

    cursor.close()
    conn.close()

    return inserted


def get_all_jobs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, company, location, link
        FROM jobs
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows