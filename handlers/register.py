from pyrogram import filters
from pyrogram.handlers import MessageHandler

from data.animations import ANIMATIONS
from handlers.commands import help_handler
from handlers.animations import animation_handler
from handlers.outgoing_messages import outgoing_handler

def register_handlers(client):
    ANIMATION_COMMANDS = [ cmd for commands in ANIMATIONS.keys() for cmd in commands ]
    
    ALL_COMMANDS = ["help"] + ANIMATION_COMMANDS

    client.add_handler(
        MessageHandler(
            help_handler,
            filters.command("help") & filters.me
        )
    )

    client.add_handler(
        MessageHandler(
            animation_handler,
            filters.me & filters.command(ANIMATION_COMMANDS)
        )
    )

    client.add_handler(
        MessageHandler(
            outgoing_handler,
            filters.me & ~filters.command(ALL_COMMANDS)
        )
    )