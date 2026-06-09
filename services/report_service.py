from database.db import get_db

def get_all_logs():
    db = get_db()
    logs = db.execute("SELECT * FROM logs ORDER BY timestamp DESC").fetchall()
    return logs

def get_user_logs(username):
    db = get_db()
    logs = db.execute(
        "SELECT * FROM logs WHERE user = ? ORDER BY timestamp DESC",
        (username,)
    ).fetchall()
    return logs