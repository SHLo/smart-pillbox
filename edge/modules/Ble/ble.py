import sys
import asyncio
import platform

from bleak import BleakClient

ADDRESS = (
    "24:71:89:cc:09:05"
    if platform.system() != "Darwin"
    else "B9EA5233-37EF-4DD6-87A8-2A875E821C46"
)


async def main(address: str):
    async with BleakClient(address) as client:
        svcs = await client.get_services()
        #print("Services:")
        for service in client.services:
            #print(service)
            for char in service.characteristics:
                print(char.description)
                if char.description == 'Digital Output':
                    await client.write_gatt_char(char.uuid, (1).to_bytes(2, byteorder='little'), False)

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) == 2 else ADDRESS))