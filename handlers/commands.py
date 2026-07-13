from utils.telegram import auto_delete
import config
from deep_translator import GoogleTranslator


async def findedKey(client, update, key: str, txt: str, txt2: str):
    st = client.lang.translate(client.user.lang, key)
    
    if key == "offBot": client.user.update(enabled = False)
    elif key == "onBot": client.user.update(enabled = True)
    elif key == "editMsgOff": client.user.update(edit_enabled = False)
    elif key == "editMsgOn": client.user.update(edit_enabled = True)
    elif key == "timeOn": client.user.update(show_time = True)
    elif key == "setTime":
        try:
            client.user.update(edit_time=int(txt))
        except: st = client.lang.translate(client.user.lang, "setTimeERROR")
    
    elif key == "editFont":
        try: 
            if len(txt) != 11: st = client.lang.translate(client.user.lang, "editFontERROR")
            else:
                client.user.update(font=txt)
        except: st = client.lang.translate(client.user.lang, "editFontERROR")


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


    elif key == "lang":
        if txt != "":
            if client.lang.exists(txt):
                client.user.update(lang = txt)
                st = client.lang.translate(client.user.lang, "langsuc")
            else:
                st = client.lang.translate(client.user.lang, "langfail")


    elif key == "translang":
        langs = GoogleTranslator().get_supported_languages(as_dict=True)

        if txt in langs.values(): 
            client.user.update(translang = txt)
            st = client.lang.translate(client.user.lang, "transsuc")
        else:
            st = client.lang.translate(client.user.lang, "transfail")
            for i in langs:
                st += f"{i}: {langs[i]}\n"


    elif key == "translator":
        await update.delete()
        
        try: 
            trans = GoogleTranslator(
                source='auto',
                target=client.user.translang
            ).translate(txt2)
        except:
            trans = txt2

        reply_id = update.reply_to_message.id if update.reply_to_message else None
        await client.send_message(update.chat.id, trans, reply_to_message_id=reply_id)
        return

    await update.edit(st)
    await auto_delete(update, 20)


async def setting_handler(bot, update):
    for key in config.KEYWORD:
        for k in config.KEYWORD[key]:
            if update.text.lower().replace("/", "").startswith(k):
                txt = update.text[len(k)+1:].replace(" ", "")
                txt2 = update.text[len(k)+2:]
                await findedKey(bot, update, key, txt, txt2); return