from database.db import get_db_connection

def save_result(user_id, exam_id, score):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO results (user_id, exam_id, score) VALUES (?, ?, ?)",
        (user_id, exam_id, score)
    )

    conn.commit()
    conn.close()


def get_results(user_id):
    conn = get_db_connection()
    results = conn.execute(
        "SELECT * FROM results WHERE user_id=?",
        (user_id,)
    ).fetchall()
    conn.close()
    return results