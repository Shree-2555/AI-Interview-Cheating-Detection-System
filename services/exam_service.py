from database.db import get_db

def create_exam(title):
    db = get_db()
    db.execute("INSERT INTO exams (title) VALUES (?)", (title,))
    db.commit()

def get_exams():
    db = get_db()
    exams = db.execute("SELECT * FROM exams").fetchall()
    return exams