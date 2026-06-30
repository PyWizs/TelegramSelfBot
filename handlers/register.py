from pyrogram import filters
from pyrogram.handlers import MessageHandler

from handlers.commands import help_handler
from handlers.animations import animation_handler

def register_handlers(client):

    client.add_handler(
        MessageHandler(
            help_handler,
            filters.command("help") & filters.me
        )
    )

    client.add_handler(
        MessageHandler(
            animation_handler,
            filters.me
        )
    )