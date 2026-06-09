from models.activity_detection import detect_activity
from database.db import get_db

def process_frame(frame):
    frame, alerts = detect_activity(frame)

    # Save alerts to DB
    db = get_db()
    for alert in alerts:
        db.execute(
            "INSERT INTO logs (user, event) VALUES (?, ?)",
            ("user", alert)
        )
    db.commit()

    return frame, alerts