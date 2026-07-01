import asyncio
from datetime import datetime


last_minute = None

async def update_client(client):
    print("updating")


async def scheduler(manager):
    global last_minute

    while True:
        minute = datetime.now().strftime("%H:%M")

        if minute != last_minute:
            last_minute = minute

            tasks = [
                update_client(client)
                for client in manager.clients.values()
            ]

            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

        await asyncio.sleep(10)