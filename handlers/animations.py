import asyncio

from data.animations import ANIMATIONS
from utils.telegram import auto_delete


async def run_animation(update, animation):
    for a in animation:
        await update.edit(a["text"])
        await asyncio.sleep(a["time"])

    await auto_delete(update, 5)


async def animation_handler(client, update):
    txt = update.text.lower()

    if txt in ANIMATIONS:
        await run_animation(update, ANIMATIONS[txt])