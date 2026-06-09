import sqlite3

def get_db():
    conn = sqlite3.connect('data/database.db')
    conn.row_factory = sqlite3.Row
    return conn

from database.db import get_db_connection

# =========================
# CREATE USER
# =========================
def create_user(username, password, role="user"):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
    """, (username, password, role))

    conn.commit()
    conn.close()


# =========================
# GET USER (LOGIN CHECK)
# =========================
def get_user(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    user = cursor.execute("""
        SELECT * FROM users WHERE username = ?
    """, (username,)).fetchone()

    conn.close()
    return user


# =========================
# GET ALL USERS (ADMIN)
# =========================
def get_all_users():
    conn = get_db_connection()

    users = conn.execute("""
        SELECT * FROM users
    """).fetchall()

    conn.close()
    return users

