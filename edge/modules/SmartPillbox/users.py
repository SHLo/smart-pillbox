import os
import io
import base64
import json
import cv2
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import azure.cosmos.cosmos_client as cosmos_client

IOTEDGE_DEVICEID = os.getenv('IOTEDGE_DEVICEID')
IOTEDGE_MODULEID = os.getenv('IOTEDGE_MODULEID')
DB_HOST = os.getenv('DB_HOST')
DB_KEY = os.getenv('DB_KEY')
DATABASE_ID = os.getenv('DATABASE_ID')
USERS_CONTAINER_ID = os.getenv('USERS_CONTAINER_ID')

FACE_ENDPOINT = os.getenv('FACE_ENDPOINT', '')
FACE_KEY = os.getenv('FACE_KEY', '')

data = []
face_client = FaceClient(FACE_ENDPOINT, CognitiveServicesCredentials(FACE_KEY))


def update_data():
    global data

    db_client = cosmos_client.CosmosClient(
        DB_HOST, {'masterKey': DB_KEY}, user_agent=IOTEDGE_MODULEID, user_agent_overwrite=True)
    db = db_client.get_database_client(DATABASE_ID)
    users_container = db.get_container_client(USERS_CONTAINER_ID)

    data_new = []

    query = f'SELECT * FROM {USERS_CONTAINER_ID} WHERE {USERS_CONTAINER_ID}.device_id = "{IOTEDGE_DEVICEID}"'

    for user in users_container.query_items(query=query, enable_cross_partition_query=True):
        img = base64.b64decode(user['photo'])
        del user['photo']
        with open(f'{user["first_name"]}.jpg', 'wb') as f:
            f.write(img)

        faces = face_client.face.detect_with_stream(io.BytesIO(img))
        user['face_id'] = faces[0].face_id

        data_new.append(user)

    data = data_new

    with open(f'users.json', 'w') as f:
        json.dump(data, f)


def match_user(img):
    _, img = cv2.imencode('.jpg', img)
    faces = face_client.face.detect_with_stream(io.BytesIO(img))

    # with open(f'curr.jpg', 'wb') as f:
    #     f.write(img)

    for face in faces:
        for user in data:
            if face_client.face.verify_face_to_face(face.face_id, user['face_id']).is_identical:
                return user


def other_user(the_user):
    for user in data:
        if user['id'] != the_user['id']:
            return user
