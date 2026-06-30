import asyncio

async def auto_delete(update, delay: int = 10):
    await asyncio.sleep(delay)

    try:
        await update.delete()
    except Exception:
        pass