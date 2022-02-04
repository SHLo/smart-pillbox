import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import logging
import cv2
import asyncio
import io
import users
from azure.iot.device import Message
import json

logger = logging.getLogger('__name__')

CV_ENDPOINT = os.getenv('CV_ENDPOINT', '')
CV_KEY = os.getenv('CV_KEY', '')

client = ComputerVisionClient(
    endpoint=CV_ENDPOINT,
    credentials=CognitiveServicesCredentials(CV_KEY)
)


def get_text(img):
    image_analysis = client.recognize_printed_text_in_stream(
        image=img,
        language='en'
    )

    ret = ''

    if len(image_analysis.regions) > 0:
        region = image_analysis.regions[0]
        lines = region.lines
        logger.warning(f'Recognized: \n')
        region_text = []
        for line in lines:
            line_text = ' '.join([word.text for word in line.words])
            logger.warning(line_text)
            region_text.append(line_text)
        ret = ' '.join(region_text).lower()

    else:
        logger.warning('Not Recognized')

    return ret


async def check_label(user, client):
    while True:
        cap = cv2.VideoCapture(0)
        _, img = cap.read()
        cap.release()
        _, img = cv2.imencode('.jpg', img)

        # with open('./a.jpg', 'wb') as f:
        #     f.write(img)

        texts = get_text(io.BytesIO(img))
        logger.warning(f'texts: {texts}')

        if user['first_name'].lower() in texts:
            text = f'Great! That is exactly the right pill pack for you!'
            await speak(text, client)
            break

        if users.other_user(user)['first_name'].lower() in texts:
            text = f'You picked the wrong tray. Please take the pill pack from the other tray'
            await speak(text, client)
            await asyncio.sleep(5)

        await asyncio.sleep(1)


async def speak(text, client):
    await client.send_message_to_output(Message(json.dumps(
        {'text': text}), content_encoding='utf-8', content_type='application/json'), 'mouth')
