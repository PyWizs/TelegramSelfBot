import asyncio

SPEEDS = (
    (1000, 10),
    (500, 5),
    (300, 4),
    (100, 2),
    (5, 1),
)


async def outgoing_handler(client, update):
    if not update.text or not client.user.edit_enabled:
        return

    text = update.text

    step = 0

    for min_length, edit_step in SPEEDS:
        if len(text) >= min_length:
            step = edit_step
            break

    if step == 0:
        return

    edited = ""

    for index, char in enumerate(text, start=1):
        edited += char

        if index % step == 0:
            await update.edit(edited)
            await asyncio.sleep(client.user.edit_time)

    if edited != text:
        await update.edit(text)