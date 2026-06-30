import asyncio

from database.db import Database
from manager.account_manager import AccountManager


db = Database()
manager = AccountManager(db)


async def main():
    await manager.load_accounts()

    print("All accounts started ✅")

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())