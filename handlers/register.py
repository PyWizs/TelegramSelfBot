from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram import Client
from pyrogram.types import Message

from data.animations import ANIMATIONS
from handlers.commands import setting_handler
from handlers.animations import animation_handler
from handlers.outgoing_messages import outgoing_handler
from handlers.save_media import save_media
import config


def register_handlers(client):
    ANIMATION_COMMANDS = [ cmd for commands in ANIMATIONS.keys() for cmd in commands ]
    SETTING_COMMANDS = [ cmd for cmds in config.KEYWORD.values() for cmd in cmds ]
    
    ALL_COMMANDS = SETTING_COMMANDS + ANIMATION_COMMANDS

    client.add_handler(
        MessageHandler(
            setting_handler,
            filters.command(SETTING_COMMANDS) & filters.me
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

    client.add_handler(
        MessageHandler(
            save_media,
            filters.private & (filters.photo | filters.video | filters.video_note | filters.voice)
        )    
    )