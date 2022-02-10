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
        'scheduled_time': get_curr_time_str()
    }

    container.create_item(body=item)


def get_last_activity(user):
    query = f'SELECT * FROM {ACTIVITIES_CONTAINER_ID} WHERE {ACTIVITIES_CONTAINER_ID}.user_id = "{user["id"]}" \
        ORDER BY {ACTIVITIES_CONTAINER_ID}.scheduled_time DESC OFFSET 0 LIMIT 1'

    [item] = container.query_items(
        query=query, enable_cross_partition_query=True)

    return item


def is_completed(user):
    return 'completed_time' in get_last_activity(user)


def get_curr_time_str():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')


def set_completed(user):
    item = get_last_activity(user)
    item['completed_time'] = get_curr_time_str()

    container.replace_item(item=item, body=item)


def get_scheduled_time(user):
    return get_last_activity(user)['scheduled_time']
