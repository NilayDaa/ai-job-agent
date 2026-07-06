from app.core.database import get_connection


def save_user_cv(user_id, filename, filepath):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_cv
        (user_id, filename, filepath)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id)
        DO UPDATE SET
            filename = EXCLUDED.filename,
            filepath = EXCLUDED.filepath,
            uploaded_at = CURRENT_TIMESTAMP
    """, (
        user_id,
        filename,
        filepath
    ))

    conn.commit()

    cursor.close()
    conn.close()


def get_user_cv(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT filename, filepath, uploaded_at
        FROM user_cv
        WHERE user_id = %s
    """, (user_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        return None

    return {
        "filename": row[0],
        "filepath": row[1],
        "uploaded_at": row[2]
    }