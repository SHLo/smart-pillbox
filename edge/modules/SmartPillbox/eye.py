import cv2
import mouth
import users

face_cascade = cv2.CascadeClassifier(
    './config/haarcascade_frontalface_default.xml')


def snap():
    cap = cv2.VideoCapture(0)
    # cap.isOpened()
    _, img = cap.read()

    if detect_face(img):
        print('face detected!')
        user = users.match_user(img)
        if user:
            mouth.speak(f'hello {user["first_name"]}')

    cap.release()


def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1,
                                          minNeighbors=5,
                                          minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)

    return len(faces) > 0
