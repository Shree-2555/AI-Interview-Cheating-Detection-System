import cv2

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

def detect_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    status = "Face Detected"

    if len(faces) == 0:
        status = "No Face Detected"
        cv2.putText(frame, status, (50,50), 1, 2, (0,0,255), 2)

    elif len(faces) > 1:
        status = "Multiple Faces Detected"
        cv2.putText(frame, status, (50,100), 1, 2, (0,0,255), 2)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

    return frame, status