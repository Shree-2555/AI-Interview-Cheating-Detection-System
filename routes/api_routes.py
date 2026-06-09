from flask import Blueprint, request, jsonify
from database.db import get_db_connection

api_bp = Blueprint("api", __name__)


@api_bp.route("/log", methods=["POST"])
def log_event():
    data = request.get_json()

    username = data.get("username", "user")
    event = data.get("event")

    if not event:
        return jsonify({"success": False, "message": "Event missing"}), 400

    db = get_db_connection()

    db.execute(
        "INSERT INTO logs (user, event) VALUES (?, ?)",
        (username, event)
    )

    db.commit()
    db.close()

    return jsonify({"success": True, "message": "Log saved"})


@api_bp.route("/report-cheat", methods=["POST"])
def report_cheat():
    print("🔥 REPORT CHEAT API CALLED")

    data = request.get_json()

    username = data.get("username")
    cheat_type = data.get("cheat_type", "Cheating Detected")

    if not username:
        return jsonify({"success": False, "message": "Username missing"}), 400

    db = get_db_connection()

    db.execute(
        "INSERT INTO logs (user, event) VALUES (?, ?)",
        (username, cheat_type)
    )

    db.execute(
        "INSERT INTO cheat_reports (username, cheat_type) VALUES (?, ?)",
        (username, cheat_type)
    )

    db.commit()
    db.close()

    return jsonify({"success": True, "message": "Cheat reported"})