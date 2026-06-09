import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

def track_eyes(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    status = "Looking Forward"

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Example: detect head movement roughly
            left_eye = face_landmarks.landmark[33]
            right_eye = face_landmarks.landmark[263]

            if abs(left_eye.x - right_eye.x) > 0.4:
                status = "Looking Away"

    cv2.putText(frame, status, (50,150), 1, 2, (255,255,0), 2)

    return frame, status