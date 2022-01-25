import cv2
import json
from azure.iot.device import Message
import users
import asyncio

face_cascade = cv2.CascadeClassifier(
    './config/haarcascade_frontalface_default.xml')


async def snap(client):
    cap = cv2.VideoCapture(0)
    # cap.isOpened()
    _, img = cap.read()

    if detect_face(img):
        print('face detected!')
        user = users.match_user(img)
        if user:
            print(f'user detected! {user}')
            text = f'hello {user["first_name"]}, please take your pills in slot {user["slot"]}'
            await client.send_message_to_output(Message(json.dumps({'text': text}), content_encoding='utf-8', content_type='application/json'), 'mouth')
            await client.send_message_to_output(Message(json.dumps({'motor': user['slot'], 'rounds': 2, 'clock_wise': True}), content_encoding='utf-8', content_type='application/json'), 'tray')
            await asyncio.sleep(5)

    cap.release()


def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1,
                                          minNeighbors=5,
                                          minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)

    return len(faces) > 0
