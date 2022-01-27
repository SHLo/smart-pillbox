import schedule
import asyncio
import users
import json
import activities
from azure.iot.device import Message

from datetime import timedelta


def remind(user, client):
    speak(user, client)

    activities.create(user)

    repeat_interval = 1

    schedule.every(repeat_interval).minutes.until(timedelta(minutes=repeat_interval * 3.5)).do(
        repeat_remind, user=user, client=client)


def speak(user, client):
    text = f'{user["first_name"]}, it is your time to take pills in tray {user["slot"]}'

    client.send_message_to_output(Message(json.dumps(
        {'text': text}), content_encoding='utf-8', content_type='application/json'), 'mouth')


def repeat_remind(user, client):
    if activities.is_completed(user):
        return schedule.CancelJob

    speak(user, client)


def reset_schedule(client):
    schedule.clear()
    users.update_data()

    for user in users.get_data():
        for t in user['schedule']['time']:
            schedule.every().day.at(t).do(remind, user=user, client=client)


async def loop():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)
