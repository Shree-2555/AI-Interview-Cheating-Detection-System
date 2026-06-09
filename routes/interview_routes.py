import os
import cv2
import numpy as np
import base64
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for

from database.db import get_db_connection

interview_bp = Blueprint("interview", __name__)

UPLOAD_FOLDER = "static/interview_videos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


@interview_bp.route("/interview")
def interview():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    return render_template("user/interview.html")


@interview_bp.route("/save-interview-video", methods=["POST"])
def save_interview_video():
    if "user" not in session:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    username = session["user"]

    if "video" not in request.files:
        return jsonify({"success": False, "message": "No video received"}), 400

    video = request.files["video"]

    filename = f"{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.webm"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    video.save(filepath)

    db = get_db_connection()
    db.execute("""
        INSERT INTO interview_videos (username, video_path)
        VALUES (?, ?)
    """, (username, filepath.replace("\\", "/")))

    db.commit()
    db.close()

    return jsonify({"success": True, "message": "Interview video saved"})


@interview_bp.route("/detect", methods=["POST"])
def detect():
    data = request.get_json()
    image_data = data["image"]

    encoded_data = image_data.split(",")[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return jsonify({"status": "❌ No face detected"})

    if len(faces) > 1:
        return jsonify({"status": "❌ Multiple faces detected"})

    (x, y, w, h) = faces[0]

    center_x = x + w // 2
    frame_center = img.shape[1] // 2
    threshold = 50

    if center_x < frame_center - threshold:
        return jsonify({"status": "⚠️ Looking LEFT"})

    if center_x > frame_center + threshold:
        return jsonify({"status": "⚠️ Looking RIGHT"})

    if y > img.shape[0] * 0.6:
        return jsonify({"status": "⚠️ Looking DOWN"})

    return jsonify({"status": "✅ Focused"})


@interview_bp.route("/save-screenshot", methods=["POST"])
def save_screenshot():
    try:
        data = request.get_json()

        if not data or "image" not in data:
            return jsonify({"error": "No image"}), 400

        image_data = data["image"]
        user = session.get("user", "Unknown")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        encoded = image_data.split(",")[1]
        img_bytes = base64.b64decode(encoded)

        folder = os.path.join("static", "screenshots")
        os.makedirs(folder, exist_ok=True)

        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
        path = os.path.join(folder, filename)

        with open(path, "wb") as f:
            f.write(img_bytes)

        db = get_db_connection()

        db.execute(
            "INSERT INTO logs (user, event, timestamp) VALUES (?, ?, ?)",
            (user, f"Screenshot: {filename}", timestamp)
        )

        db.commit()
        db.close()

        print(f"✅ Saved screenshot: {filename} | User: {user}")

        return jsonify({"message": "saved"})

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500