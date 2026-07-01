import asyncio

from pyrogram import Client
from pyrogram.errors import (
    SessionPasswordNeeded,
    PhoneCodeInvalid,
    PhoneCodeExpired
)

from config import API_ID, API_HASH
from database.db import Database

db = Database()


async def main():
    phone = input("Phone Number: ")

    app = Client(
        name="temp_login",
        api_id=API_ID,
        api_hash=API_HASH
    )

    await app.connect()

    sent_code = await app.send_code(phone)

    code = input("Code: ").replace(" ", "")

    try:
        await app.sign_in(
            phone_number=phone,
            phone_code_hash=sent_code.phone_code_hash,
            phone_code=code
        )

    except SessionPasswordNeeded:
        password = input("2FA Password: ")
        await app.check_password(password)

    except PhoneCodeInvalid:
        print("Invalid Code")
        await app.disconnect()
        return

    except PhoneCodeExpired:
        print("Code Expired")
        await app.disconnect()
        return

    me = await app.get_me()

    session_string = await app.export_session_string()

    db.add_account(
        user_id=me.id,
        session_string=session_string
    )

    print(f"{me.first_name} Added Successfully!")

    await app.disconnect()


if __name__ == "__main__":
    asyncio.run(main())