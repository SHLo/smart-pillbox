import schedule
import asyncio
import users
import json
import activities
import logging
from azure.iot.device import Message

from datetime import timedelta

logger = logging.getLogger('__name__')


def remind(user, client, scheduled_time=None):

    logger.warning(f'reminde {user["first_name"]}')
    notify(user, client)
    client.send_message_to_output(Message(json.dumps(
        {'motor': user['tray'], 'rounds': 1 / 21, 'clock_wise': True}), content_encoding='utf-8', content_type='application/json'), 'tray')

    activities.create(user, scheduled_time)

    repeat_interval = 1

    schedule.every(repeat_interval).minutes.until(timedelta(minutes=repeat_interval * 3.5)).do(
        repeat_remind, user=user, client=client)


def notify(user, client):
    tray = user['tray']
    text = f'{user["first_name"]}, it is your time to take pills in {tray} tray'

    client.send_message_to_output(Message(json.dumps(
        {'text': text}), content_encoding='utf-8', content_type='application/json'), 'mouth')
    client.send_message_to_output(Message(json.dumps(
        {'tray': tray}), content_encoding='utf-8', content_type='application/json'), 'ble')


def repeat_remind(user, client):
    if activities.is_completed(user):
        logger.warning(
            f'{user["first_name"]} has completed, cancel the repeat reminder')
        return schedule.CancelJob

    logger.warning(f'reminde {user["first_name"]} repeatly')
    notify(user, client)


def reset_schedule(client):
    schedule.clear()
    users.update_data()

    for user in users.get_data():
        for t in user['schedule']['time']:
            schedule.every().day.at(t).do(remind, user=user, client=client)
            logger.warning(f'set reminder for {user["first_name"]} at {t}')


async def loop():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)
