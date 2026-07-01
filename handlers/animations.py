import asyncio
import re

from data.animations import ANIMATIONS
from utils.telegram import auto_delete


def get_run(text: str):
    match = re.search(r"--run\s+(\d+)", text)
    return int(match.group(1)) if match else None


def get_message(text: str):
    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        return ""

    message = parts[1]

    message = re.sub(r"\s*--run\s+\d+", "", message).strip()

    if "<a>" not in message:
        message += " <a>" if message else "<a>"

    return message


async def run_animation(update, animation: dict, txt: str):
    message = get_message(txt)

    run = get_run(txt)
    if run is None:
        run = animation["run"]

    for _ in range(run):
        for frame in animation["animation"]:
            try: await update.edit(message.replace("<a>", frame["text"]))
            except: break

            await asyncio.sleep(frame["time"])

    if message == "<a>":
        await auto_delete(update, 5)


async def animation_handler(client, update):
    if not update.text:
        return

    command = update.text.split()[0].lstrip("/").lower()

    for commands, animation in ANIMATIONS.items():
        if command in commands:
            await run_animation(update, animation, update.text)
            return