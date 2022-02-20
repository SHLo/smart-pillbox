# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import asyncio
import reminder
import sys
import signal
import threading
import json
from azure.iot.device import IoTHubModuleClient, MethodResponse
import logging
import users


# Event indicating client stop
stop_event = threading.Event()

logger = logging.getLogger('__name__')


def create_client():
    client = IoTHubModuleClient.create_from_edge_environment()

    # Define function for handling received messages
    def receive_message_handler(message):
        # NOTE: This function only handles messages sent to 'input1'.
        # Messages sent to other inputs, or to the default, will be discarded
        if message.input_name == 'script':
            logger.warning('the data in the message received on script was ')
            logger.warning(message.data)
            logger.warning('custom properties are')
            logger.warning(message.custom_properties)

    def method_request_handler(method_request):
        request_name = method_request.name
        request_payload = method_request.payload

        logger.warning(
            f'receive direct method: {request_name}, {request_payload}')

        if request_name == 'remind':
            status = 200
            try:
                user = users.get_user(request_payload['first_name'])
                reminder.remind(user, client, request_payload['schedule_time'])
            except:
                status = 400

        method_response = MethodResponse.create_from_method_request(
            method_request, status, {})
        client.send_method_response(method_response)

    try:
        # Set handler on the client
        client.on_message_received = receive_message_handler
        client.on_method_request_received = method_request_handler
    except:
        # Cleanup if failure occurs
        client.shutdown()
        raise

    return client


async def run_sample(client):
    # Customize this coroutine to do whatever tasks the module initiates
    # e.g. sending messages
    reminder.reset_schedule(client)
    await reminder.loop()


def main():
    logger.warning('IoT Hub Client for Python')

    # NOTE: Client is implicitly connected due to the handler being set on it
    client = create_client()

    # Define a handler to cleanup when module is is terminated by Edge
    def module_termination_handler(signal, frame):
        logger.warning('IoTHubClient sample stopped by Edge')
        stop_event.set()

    # Set the Edge termination handler
    signal.signal(signal.SIGTERM, module_termination_handler)

    # Run the sample
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_sample(client))
    except Exception as e:
        logger.warning('Unexpected error %s ' % e)
        raise
    finally:
        logger.warning('Shutting down IoT Hub Client...')
        client.shutdown()
        loop.close()


if __name__ == '__main__':
    main()
