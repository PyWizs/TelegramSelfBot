async def save_media(client, update):
    file_path = await update.download()
    caption = update.caption if update.caption else ""

    if update.photo and update.photo.ttl_seconds:
        await client.send_photo("me", file_path, caption=caption)
    elif update.video and update.video.ttl_seconds:
        await client.send_video("me", file_path, caption=caption)
    elif update.video_note and update.video_note.ttl_seconds:
        await client.send_video("me", file_path)
    elif update.voice and update.voice.ttl_seconds:
        await client.send_voice("me", file_path)
