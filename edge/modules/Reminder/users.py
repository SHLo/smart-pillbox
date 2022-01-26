import os
import io
import json
import azure.cosmos.cosmos_client as cosmos_client

IOTEDGE_DEVICEID = os.getenv('IOTEDGE_DEVICEID')
IOTEDGE_MODULEID = os.getenv('IOTEDGE_MODULEID')
DB_HOST = os.getenv('DB_HOST')
DB_KEY = os.getenv('DB_KEY')
DATABASE_ID = os.getenv('DATABASE_ID')
USERS_CONTAINER_ID = os.getenv('USERS_CONTAINER_ID')

data = []


def update_data():
    global data

    db_client = cosmos_client.CosmosClient(
        DB_HOST, {'masterKey': DB_KEY}, user_agent=IOTEDGE_MODULEID, user_agent_overwrite=True)
    db = db_client.get_database_client(DATABASE_ID)
    users_container = db.get_container_client(USERS_CONTAINER_ID)

    data_new = []

    query = f'SELECT * FROM {USERS_CONTAINER_ID} WHERE {USERS_CONTAINER_ID}.device_id = "{IOTEDGE_DEVICEID}"'

    for user in users_container.query_items(query=query, enable_cross_partition_query=True):
        del user['photo']

        data_new.append(user)

    data = data_new

    with open(f'users.json', 'w') as f:
        json.dump(data, f)


def get_data():
    return data
