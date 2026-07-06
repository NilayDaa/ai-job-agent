from app.core.database import get_connection


def create_user(username, email, password_hash):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users
        (username, email, password_hash)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (
        username,
        email,
        password_hash
    ))

    user_id = cursor.fetchone()[0]

    conn.commit()

    cursor.close()
    conn.close()

    return user_id
def username_exists(username):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username=%s",
        (username,)
    )

    exists = cursor.fetchone()

    cursor.close()
    conn.close()

    return exists is not None


def email_exists(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE email=%s",
        (email,)
    )

    exists = cursor.fetchone()

    cursor.close()
    conn.close()

    return exists is not None

def get_user_by_email(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username, email, password_hash
        FROM users
        WHERE email = %s
    """, (email,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "username": row[1],
        "email": row[2],
        "password_hash": row[3]
    }