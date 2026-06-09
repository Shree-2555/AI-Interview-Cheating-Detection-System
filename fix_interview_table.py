from database.db import get_db_connection

db = get_db_connection()

db.execute("""
CREATE TABLE IF NOT EXISTS interview_videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    video_path TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

db.commit()
db.close()

print("interview_videos table created ✔️")