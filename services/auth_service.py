from werkzeug.security import check_password_hash
from database.db import get_user

def login_user(username, password):
    user = get_user(username)

    if not user:
        return "no_user"

    if not check_password_hash(user['password'], password):
        return "wrong_password"

    return user

from werkzeug.security import check_password_hash
from database.db import get_user

def login_user(username, password):
    user = get_user(username)

    if not user:
        return "no_user"

    # 🔥 IMPORTANT LINE
    if not check_password_hash(user['password'], password):
        return "wrong_password"

    return user

def login_user(username, password):
    user = get_user(username)

    print("Entered:", password)
    print("Stored:", user['password'] if user else "No user")

    if not user:
        return "no_user"

    if user['password'] != password:
        return "wrong_password"

    return user