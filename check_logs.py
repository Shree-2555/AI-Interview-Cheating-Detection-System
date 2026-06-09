from database.db import get_db_connection

db = get_db_connection()

logs = db.execute("SELECT * FROM logs ORDER BY id DESC").fetchall()

if not logs:
    print("❌ No logs found")
else:
    for log in logs:
        print(dict(log))

db.close()