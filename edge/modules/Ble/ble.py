import sys
import asyncio
import platform
import os

from bleak import BleakClient


ADDRESS_A = os.getenv('ADDRESS_A', '')
ADDRESS_B = os.getenv('ADDRESS_B', '')


async def remind(tray):
    address = {'a': ADDRESS_A, 'b': ADDRESS_B}[tray]

    async with BleakClient(address) as client:
        for service in client.services:
            for char in service.characteristics:
                if char.description == 'Digital Output':
                    await client.write_gatt_char(char.uuid, (1).to_bytes(2, byteorder='little'))
