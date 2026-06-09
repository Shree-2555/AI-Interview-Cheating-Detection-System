from database.db import get_db_connection

db = get_db_connection()

db.execute("DELETE FROM logs WHERE event = ?", ("Manual Test Cheat",))
db.execute("DELETE FROM cheat_reports WHERE cheat_type = ?", ("Manual Test Cheat",))

db.commit()
db.close()

print("Dummy alerts cleared ✔️")