import asyncio
from datetime import datetime

last_minute = None

def format_time(font: list):
    current_time = datetime.now().strftime('%H:%M')
    mapping = {str(i): font[i] for i in range(10)}
    mapping[":"] = font[10]
    return "".join(mapping.get(ch, ch) for ch in current_time)


async def update_client(client):
    if not (client.user.enabled and client.user.show_time): return

    me = await client.get_me()
    name = me.first_name

    for f in client.user.font: name = name.replace(f, "")

    t = format_time(client.user.font)
    
    await client.update_profile(first_name=f"{name} {t}"[:64])


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

        await asyncio.sleep(5)