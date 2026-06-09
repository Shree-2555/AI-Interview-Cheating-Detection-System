from datetime import datetime, timedelta
from flask import Blueprint, render_template, session, redirect, url_for, request
from database.db import get_db_connection

user_bp = Blueprint("user", __name__)


@user_bp.route("/")
@user_bp.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    username = session["user"]
    db = get_db_connection()

    results = db.execute("""
        SELECT id, exam_id, exam_name, score, total_marks, status, created_at
        FROM results
        WHERE username = ?
        ORDER BY id DESC
    """, (username,)).fetchall()

    exam_history = []

    for row in results:
        score = row["score"]
        total_marks = row["total_marks"]
        percentage = (score / total_marks) * 100 if total_marks > 0 else 0

        exam_history.append({
            "name": row["exam_name"] if row["exam_name"] else "Unknown Exam",
            "score": score,
            "total_marks": total_marks,
            "percentage": round(percentage, 2),
            "status": row["status"] if row["status"] else ("Pass" if percentage >= 40 else "Fail"),
            "date": row["created_at"]
        })

    logs = db.execute("""
        SELECT event, timestamp
        FROM logs
        WHERE user = ?
        ORDER BY id DESC
        LIMIT 10
    """, (username,)).fetchall()

    alerts = []

    for log in logs:
        utc_time = datetime.strptime(log["timestamp"], "%Y-%m-%d %H:%M:%S")
        india_time = utc_time + timedelta(hours=5, minutes=30)

        alerts.append({
            "type": log["event"],
            "time": india_time.strftime("%d %b %Y, %I:%M %p")
        })

    db.close()

    return render_template(
        "user/dashboard.html",
        username=username,
        exams=exam_history,
        alerts=alerts
    )


@user_bp.route("/interview")
def start_interview():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    return render_template("user/interview.html")


@user_bp.route("/exams")
def view_exams():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    db = get_db_connection()
    exams = db.execute("SELECT * FROM exams").fetchall()
    db.close()

    return render_template("user/exams.html", exams=exams)


@user_bp.route("/exam/<int:exam_id>")
def start_exam(exam_id):
    if "user" not in session:
        return redirect(url_for("auth.login"))

    db = get_db_connection()

    questions = db.execute(
        "SELECT * FROM questions WHERE exam_id = ?",
        (exam_id,)
    ).fetchall()

    db.close()

    return render_template(
        "user/exam.html",
        questions=questions,
        exam_id=exam_id
    )


@user_bp.route("/submit-exam/<int:exam_id>", methods=["POST"])
def submit_exam(exam_id):
    if "user" not in session:
        return redirect(url_for("auth.login"))

    username = session["user"]
    db = get_db_connection()

    exam = db.execute(
        "SELECT title FROM exams WHERE id = ?",
        (exam_id,)
    ).fetchone()

    exam_name = exam["title"] if exam else "Unknown Exam"

    questions = db.execute(
        "SELECT * FROM questions WHERE exam_id = ?",
        (exam_id,)
    ).fetchall()

    score = 0
    total_marks = len(questions)

    for q in questions:
        user_answer = request.form.get(f"q{q['id']}")
        if user_answer == q["correct_answer"]:
            score += 1

    percentage = (score / total_marks) * 100 if total_marks > 0 else 0
    status = "Pass" if percentage >= 40 else "Fail"

    db.execute("""
        INSERT INTO results 
        (username, exam_id, exam_name, score, total_marks, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        username,
        exam_id,
        exam_name,
        score,
        total_marks,
        status
    ))

    db.commit()
    db.close()

    return redirect(url_for("user.result"))


@user_bp.route("/result")
def result():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    username = session["user"]
    db = get_db_connection()

    result = db.execute("""
        SELECT *
        FROM results
        WHERE username = ?
        ORDER BY id DESC
        LIMIT 1
    """, (username,)).fetchone()

    db.close()

    return render_template("user/result.html", result=result)