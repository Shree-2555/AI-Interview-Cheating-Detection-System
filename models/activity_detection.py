from models.face_detection import detect_face
from models.eye_tracking import track_eyes
from models.audio_detection import detect_audio

def detect_activity(frame):
    alerts = []

    # Face Detection
    frame, face_status = detect_face(frame)
    if face_status != "Face Detected":
        alerts.append(face_status)

    # Eye Tracking
    frame, eye_status = track_eyes(frame)
    if eye_status == "Looking Away":
        alerts.append(eye_status)

    # Audio Detection
    try:
        audio_status = detect_audio()
        if audio_status == "Noise Detected":
            alerts.append(audio_status)
    except:
        audio_status = "Audio Error"

    return frame, alerts