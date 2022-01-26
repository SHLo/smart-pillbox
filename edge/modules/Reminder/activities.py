import os
import azure.cosmos.cosmos_client as cosmos_client
import uuid
import datetime

IOTEDGE_DEVICEID = os.getenv('IOTEDGE_DEVICEID')
IOTEDGE_MODULEID = os.getenv('IOTEDGE_MODULEID')
DB_HOST = os.getenv('DB_HOST')
DB_KEY = os.getenv('DB_KEY')
DATABASE_ID = os.getenv('DATABASE_ID')
ACTIVITIES_CONTAINER_ID = os.getenv('ACTIVITIES_CONTAINER_ID')

db_client = cosmos_client.CosmosClient(
    DB_HOST, {'masterKey': DB_KEY}, user_agent=IOTEDGE_MODULEID, user_agent_overwrite=True)
db = db_client.get_database_client(DATABASE_ID)
container = db.get_container_client(ACTIVITIES_CONTAINER_ID)


def create(user):
    now = datetime.datetime.now()

    item = {
        'id': str(uuid.uuid4()),
        'user_id': user['id'],
        'scheduled_time': now.strftime('%Y-%m-%d %H:%M')
    }

    container.create_item(body=item)
