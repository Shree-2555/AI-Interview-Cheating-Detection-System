import os
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, session
from database.db import get_db_connection

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
@admin_bp.route('/dashboard')
def admin_dashboard():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    db = get_db_connection()

    try:
        users_count = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    except:
        users_count = 0

    try:
        questions_count = db.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    except:
        questions_count = 0

    try:
        alerts_count = db.execute("SELECT COUNT(*) FROM logs").fetchone()[0]
    except:
        alerts_count = 0

    try:
        users = db.execute("SELECT id, username, role FROM users").fetchall()
    except:
        users = []

    try:
        logs_data = db.execute("""
            SELECT user, COUNT(*) as count, MAX(timestamp) as last_time
            FROM logs
            GROUP BY user
            ORDER BY count DESC
        """).fetchall()

        logs = []
        leaderboard = []

        for log in logs_data:
            utc_time = datetime.strptime(log["last_time"], "%Y-%m-%d %H:%M:%S")
            india_time = utc_time + timedelta(hours=5, minutes=30)

            cheat_text = "Cheat" if log["count"] == 1 else "Cheats"

            logs.append({
                "user": log["user"],
                "event": f"{log['count']} {cheat_text}",
                "count": log["count"],
                "time": india_time.strftime("%d %b %Y, %I:%M %p")
            })

            leaderboard.append({
                "user": log["user"],
                "count": log["count"]
            })

    except:
        logs = []
        leaderboard = []

    db.close()

    return render_template(
        "admin/dashboard.html",
        users_count=users_count,
        questions_count=questions_count,
        alerts_count=alerts_count,
        users=users,
        logs=logs,
        leaderboard=leaderboard
    )


@admin_bp.route('/results')
def admin_results():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    db = get_db_connection()

    results = db.execute("""
        SELECT 
            username,
            exam_name,
            score,
            total_marks,
            status,
            created_at,
            ROUND((score * 100.0 / total_marks), 2) AS percentage
        FROM results
        ORDER BY percentage DESC
    """).fetchall()

    top_performer = db.execute("""
        SELECT 
            username,
            exam_name,
            score,
            total_marks,
            status,
            created_at,
            ROUND((score * 100.0 / total_marks), 2) AS percentage
        FROM results
        ORDER BY percentage DESC
        LIMIT 1
    """).fetchone()

    db.close()

    return render_template(
        "admin/results.html",
        results=results,
        top_performer=top_performer
    )


@admin_bp.route('/interview-videos')
def interview_videos():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    db = get_db_connection()

    videos = db.execute("""
        SELECT *
        FROM interview_videos
        ORDER BY id DESC
    """).fetchall()

    db.close()

    return render_template(
        "admin/interview_videos.html",
        videos=videos
    )


@admin_bp.route('/delete-user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    db = get_db_connection()

    user = db.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    if user and user['role'] != 'admin':
        db.execute("DELETE FROM users WHERE id = ?", (user_id,))
        db.commit()

    db.close()
    return redirect(url_for('admin.admin_dashboard'))


@admin_bp.route('/cheating')
def cheating():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    folder = os.path.join("static", "screenshots")
    images = []

    if os.path.exists(folder):
        images = os.listdir(folder)

    images = sorted(images, reverse=True)

    return render_template("admin/cheating.html", images=images)


@admin_bp.route('/create-exam', methods=['GET', 'POST'])
def create_exam():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    db = get_db_connection()

    if request.method == 'POST':
        title = request.form['title']

        db.execute("INSERT INTO exams (title) VALUES (?)", (title,))
        db.commit()

        exam_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        db.close()

        return redirect(url_for('admin.add_question', exam_id=exam_id))

    db.close()
    return render_template('admin/create_exam.html')


@admin_bp.route('/add-question/<int:exam_id>', methods=['GET', 'POST'])
def add_question(exam_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    db = get_db_connection()

    if request.method == 'POST':
        question = request.form['question']
        option_a = request.form['option_a']
        option_b = request.form['option_b']
        option_c = request.form['option_c']
        option_d = request.form['option_d']
        correct_answer = request.form['correct_answer']

        db.execute("""
            INSERT INTO questions (
                exam_id, question, option_a, option_b, option_c, option_d, correct_answer
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            exam_id,
            question,
            option_a,
            option_b,
            option_c,
            option_d,
            correct_answer
        ))

        db.commit()
        db.close()

        return redirect(url_for('admin.add_question', exam_id=exam_id))

    db.close()
    return render_template('admin/add_question.html', exam_id=exam_id)