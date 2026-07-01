from utils.telegram import auto_delete
import config


async def findedKey(client, update, key: str):
    st = config.TEXTSETTING[key]

    if key == "offBot": client.user.update(enabled = False)
    elif key == "onBot": client.user.update(enabled = True)
    elif key == "editMsgOff": client.user.update(edit_enabled = False)
    elif key == "editMsgOn": client.user.update(edit_enabled = True)
    elif key == "timeOn": client.user.update(show_time = True)
    elif key == "timeOff": 
        me = await client.get_me()
        name = me.first_name

        for f in client.user.font: name = name.replace(f, "")
        await client.update_profile(first_name=f"{name}"[:64])
        
        client.user.update(show_time = False)
    
    elif key == "vaziat":
        client.user.reload()
        st = st.format(
            "✅" if client.user.enabled else "❌",
            "✅" if client.user.show_time else "❌",
            "✅" if client.user.edit_enabled else "❌",
            client.user.edit_time,
            client.user.font
        )

    await update.edit(st)
    await auto_delete(update)


async def setting_handler(bot, update):
    for key in config.KEYWORD:
        for k in config.KEYWORD[key]:
            if update.text.lower().replace("/", "").startswith(k):
                await findedKey(bot, update, key); break