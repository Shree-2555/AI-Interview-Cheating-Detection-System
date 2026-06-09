from datetime import datetime

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_log(user, event):
    return f"{get_current_time()} | {user} | {event}"


def is_admin(user):
    return user.get('role') == 'admin'