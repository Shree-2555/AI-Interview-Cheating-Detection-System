from database.db import get_db_connection

def save_log(user_id, log_type, message):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO logs (user_id, type, message) VALUES (?, ?, ?)",
        (user_id, log_type, message)
    )

    conn.commit()
    conn.close()


def get_logs():
    conn = get_db_connection()
    logs = conn.execute("SELECT * FROM logs").fetchall()
    conn.close()
    return logs