# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import asyncio
import sys
import signal
import threading
import os
from azure.iot.device.aio import IoTHubModuleClient
import azure.cosmos.cosmos_client as cosmos_client
import base64
import cv2
import logging
import mouth

logger = logging.getLogger('__name__')

IOTEDGE_DEVICEID = os.getenv('IOTEDGE_DEVICEID')
IOTEDGE_MODULEID = os.getenv('IOTEDGE_MODULEID')
DB_HOST = os.getenv('DB_HOST')
DB_KEY = os.getenv('DB_KEY')
DATABASE_ID = os.getenv('DATABASE_ID')
USERS_CONTAINER_ID = os.getenv('USERS_CONTAINER_ID')

# Event indicating client stop
stop_event = threading.Event()

users = []


def create_client():
    client = IoTHubModuleClient.create_from_edge_environment()

    # Define function for handling received messages
    async def receive_message_handler(message):
        # NOTE: This function only handles messages sent to "input1".
        # Messages sent to other inputs, or to the default, will be discarded
        if message.input_name == "input1":
            print("the data in the message received on input1 was ")
            print(message.data)
            print("custom properties are")
            print(message.custom_properties)
            print("forwarding mesage to output1")
            await client.send_message_to_output(message, "output1")

    try:
        # Set handler on the client
        client.on_message_received = receive_message_handler
    except:
        # Cleanup if failure occurs
        client.shutdown()
        raise

    return client


async def run_sample(client, cap):
    # Customize this coroutine to do whatever tasks the module initiates
    # e.g. sending messages

    face_cascade = cv2.CascadeClassifier(
        './config/haarcascade_frontalface_default.xml')

    while cap.isOpened():
        print('loop')
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1,
                                              minNeighbors=5,
                                              minSize=(30, 30),
                                              flags=cv2.CASCADE_SCALE_IMAGE)
        print(len(faces))
        if len(faces) > 0:
            print('face detected!')
            mouth.speak('hello world')

        await asyncio.sleep(1)


def update_user_data():
    global users

    db_client = cosmos_client.CosmosClient(
        DB_HOST, {'masterKey': DB_KEY}, user_agent=IOTEDGE_MODULEID, user_agent_overwrite=True)
    db = db_client.get_database_client(DATABASE_ID)
    users_container = db.get_container_client(USERS_CONTAINER_ID)

    users_new = []

    query = f'SELECT * FROM {USERS_CONTAINER_ID} WHERE {USERS_CONTAINER_ID}.device_id = "{IOTEDGE_DEVICEID}"'

    for user in users_container.query_items(query=query, enable_cross_partition_query=True):
        user['photo'] = base64.b64decode(user['photo'].encode('utf-8'))
        users_new.append(user)

    users = users_new


def main():
    print("IoT Hub Client for Python")

    # NOTE: Client is implicitly connected due to the handler being set on it
    client = create_client()

    # Define a handler to cleanup when module is is terminated by Edge
    def module_termination_handler(signal, frame):
        print("IoTHubClient sample stopped by Edge")
        cap.release()
        stop_event.set()

    # Set the Edge termination handler
    signal.signal(signal.SIGTERM, module_termination_handler)

    update_user_data()
    # Run the sample
    cap = cv2.VideoCapture(0)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_sample(client, cap))
    except Exception as e:
        print("Unexpected error %s " % e)
        raise
    finally:
        print("Shutting down IoT Hub Client...")
        loop.run_until_complete(client.shutdown())
        loop.close()


if __name__ == "__main__":
    main()
