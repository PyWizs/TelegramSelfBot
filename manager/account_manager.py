from pyrogram import Client

from config import API_ID, API_HASH
from handlers.register import register_handlers


class AccountManager:
    def __init__(self, db):
        self.db = db
        self.clients = {}


    async def load_accounts(self):
        accounts = self.db.get_all_accounts()

        for account in accounts:
            await self.add_account(account)


    async def add_account(self, account):

        if account["user_id"] in self.clients:
            return

        client = Client(
            name=f"user_{account['user_id']}",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=account["session_string"]
        )

        register_handlers(client)

        await client.start()

        self.clients[account["user_id"]] = client

        print(f"{account['user_id']} Started")


    def get_client(self, user_id):
        return self.clients.get(user_id)
