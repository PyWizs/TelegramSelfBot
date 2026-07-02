import asyncio

from pyrogram import Client

from config import API_ID, API_HASH
from handlers.register import register_handlers
from database.db import User
from manager.language_manager import LanguageManager

class AccountManager:
    def __init__(self, db):
        self.db = db
        self.clients = {}


    async def load_accounts(self):
        accounts = self.db.get_all_accounts()

        for account in accounts:
            if account["user_id"] not in self.clients:
                await self.add_account(account)


    async def sync_accounts(self):
        while True:
            accounts = self.db.get_all_accounts()

            for account in accounts:
                if account["user_id"] not in self.clients:
                    await self.add_account(account)

            await asyncio.sleep(1800)

    async def add_account(self, account):
        if account["user_id"] in self.clients:
            return

        client = Client(
            name=f"user_{account['user_id']}",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=account["session_string"]
        )

        client.user = User(self.db, account["user_id"])
        client.lang = LanguageManager(default_language=client.user.lang)

        await client.start()

        register_handlers(client)

        self.clients[account["user_id"]] = client

        print(f"{account['user_id']} Started")


    def get_client(self, user_id):
        return self.clients.get(user_id)
