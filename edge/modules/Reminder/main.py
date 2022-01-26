# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import asyncio
import sys
import signal
import threading
import json
import reminder


# Event indicating client stop
stop_event = threading.Event()


async def run_sample():
    # Customize this coroutine to do whatever tasks the module initiates
    # e.g. sending messages
    reminder.set_schedule()
    await reminder.loop()


def main():
    # Define a handler to cleanup when module is is terminated by Edge
    def module_termination_handler(signal, frame):
        print("IoTHubClient sample stopped by Edge")
        stop_event.set()

    # Set the Edge termination handler
    signal.signal(signal.SIGTERM, module_termination_handler)

    # Run the sample
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_sample())
    except Exception as e:
        print("Unexpected error %s " % e)
        raise
    finally:
        loop.close()


if __name__ == "__main__":
    main()
