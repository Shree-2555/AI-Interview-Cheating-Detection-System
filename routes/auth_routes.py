from flask import Blueprint, render_template, request, redirect, session
from database.db import get_db
from services.auth_service import login_user

auth_bp = Blueprint('auth', __name__)

# =========================
# LOGIN
# =========================
@auth_bp.route('/', methods=['GET', 'POST'])
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        result = login_user(username, password)

        if result == "no_user":
            error = "User not found"
        elif result == "wrong_password":
            error = "Invalid password"
        elif not result:
            error = "Something went wrong"
        else:
            session['user'] = result['username']
            session['role'] = result['role']

            print("SESSION SET:", session.get('user'))

            if result['role'] == 'admin':
                return redirect('/admin')
            return redirect('/user/dashboard')

    return render_template('login.html', error=error)


# =========================
# REGISTER
# =========================
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            error = "All fields are required"
            return render_template('register.html', error=error)

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user:
            error = "Username already exists"
        else:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, 'user')
            )
            db.commit()
            db.close()
            return redirect('/login')

        db.close()

    return render_template('register.html', error=error)


# =========================
# LOGOUT
# =========================
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')