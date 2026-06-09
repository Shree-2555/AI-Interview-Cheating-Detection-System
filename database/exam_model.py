from database.db import get_db_connection

def create_exam(title, description):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO exams (title, description) VALUES (?, ?)",
        (title, description)
    )

    conn.commit()
    conn.close()


def get_exams():
    conn = get_db_connection()
    exams = conn.execute("SELECT * FROM exams").fetchall()
    conn.close()
    return exams


def add_question(exam_id, question, o1, o2, o3, o4, answer):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO questions 
        (exam_id, question, option1, option2, option3, option4, answer)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (exam_id, question, o1, o2, o3, o4, answer))

    conn.commit()
    conn.close()


def get_questions(exam_id):
    conn = get_db_connection()
    questions = conn.execute(
        "SELECT * FROM questions WHERE exam_id=?",
        (exam_id,)
    ).fetchall()
    conn.close()
    return questions