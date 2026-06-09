from datetime import datetime
from database.db import get_db

def log_to_file(message):
    with open('logs/activity.log', 'a') as f:
        f.write(f"{datetime.now()} - {message}\n")


def log_to_db(user, event):
    db = get_db()
    db.execute(
        "INSERT INTO logs (user, event) VALUES (?, ?)",
        (user, event)
    )
    db.commit()


def log_error(error):
    with open('logs/error.log', 'a') as f:
        f.write(f"{datetime.now()} - ERROR: {error}\n")