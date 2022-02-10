import cv2
import json
from azure.iot.device import Message
import users
import asyncio
import activities
import logging
import ocr

logger = logging.getLogger('__name__')

face_cascade = cv2.CascadeClassifier(
    './config/haarcascade_frontalface_default.xml')


async def snap(client):
    cap = cv2.VideoCapture(0)
    # cap.isOpened()
    _, img = cap.read()
    cap.release()

    if detect_face(img):
        logger.warning('face detected!')
        user = users.match_user(img)
        if user:
            logger.warning(f'user detected! {user}')
            if not activities.is_completed(user):
                await client.send_message_to_output(Message(json.dumps({'motor': user['slot'], 'rounds': 1 / 21, 'clock_wise': True}), content_encoding='utf-8', content_type='application/json'), 'tray')
                text = f'hello {user["first_name"]}, please take your pills in tray {user["slot"]}, and put the label in front of the camera'
                await speak(text, client)

                await ocr.check_label(user, client)

                activities.set_completed(user)

                await asyncio.sleep(5)

            else:
                text = f'hello {user["first_name"]}, you have taken your pills. Please wait for the next reminder'
                await speak(text, client)


async def speak(text, client):
    await client.send_message_to_output(Message(json.dumps(
        {'text': text}), content_encoding='utf-8', content_type='application/json'), 'mouth')
    await asyncio.sleep(5)


def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1,
                                          minNeighbors=5,
                                          minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)

    return len(faces) > 0
