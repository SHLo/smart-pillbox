import schedule
import asyncio
import users
import json
import activities
from azure.iot.device import Message
from azure.iot.device import IoTHubModuleClient

import datetime

module_client = IoTHubModuleClient.create_from_edge_environment()
module_client.connect()


def remind(user):
    text = f'{user["first_name"]}, it is your time to take pills in tray {user["slot"]}'

    module_client.send_message_to_output(Message(json.dumps(
        {'text': text}), content_encoding='utf-8', content_type='application/json'), 'mouth')

    activities.create(user)


def set_schedule():
    users.update_data()

    for user in users.get_data():
        for t in user['schedule']['time']:
            schedule.every().day.at(t).do(remind, user=user)


async def loop():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)
