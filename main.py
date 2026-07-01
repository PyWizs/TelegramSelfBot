import asyncio

from database.db import Database
from manager.account_manager import AccountManager
from manager.time_manager import scheduler

db = Database()
manager = AccountManager(db)


async def main():
    await manager.load_accounts()

    print("All accounts started ✅")

    asyncio.create_task(manager.sync_accounts())
    asyncio.create_task(scheduler(manager))

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())