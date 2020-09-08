from userge import userge, Config, get_collection, Message
from pyrogram.types import CallbackQuery
from pyrogram import filters
import json
import os

SECRETS = "userge/xcache/secrets.txt"


if Config.BOT_TOKEN and Config.OWNER_ID:
    if Config.HU_STRING_SESSION:
        ubot = userge.bot
    else:
        ubot = userge

       
<<<<<<< HEAD:userge/plugins/Satır İçi/secret.py
    @ubot.on_callback_query(filters.regex(pattern=r"^secret_btn$"))
    async def alive_callback(_, callback_query: CallbackQuery): 
        sender = await userge.get_me()
        msg = f"🔓 **{sender.first_name}** : tarafından gelen mesaj "
        if sender.last_name:
            msg += f" {sender.last_name}\n"
        else:
            msg += "\n"
        async for data in SECRET_MSG.find():
            receiver = data['user_id']
||||||| e151c67:userge/plugins/inline/secret.py
    @ubot.on_callback_query(filters.regex(pattern=r"^secret_btn$"))
    async def alive_callback(_, callback_query: CallbackQuery): 
        sender = await userge.get_me()
        msg = f"🔓 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 𝗳𝗿𝗼𝗺: {sender.first_name}"
        if sender.last_name:
            msg += f" {sender.last_name}\n"
        else:
            msg += "\n"
        async for data in SECRET_MSG.find():
            receiver = data['user_id']
=======
    @ubot.on_callback_query(filters.regex(pattern=r"^secret_(.*)"))
    async def alive_callback(_, c_q: CallbackQuery):
        msg_id = c_q.matches[0].group(1)
        if os.path.exists(SECRETS):
            view_data = json.load(open(SECRETS))
            sender = await userge.get_me()
            msg = f"🔓 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 𝗳𝗿𝗼𝗺: {sender.first_name}"
            if sender.last_name:
                msg += f" {sender.last_name}\n"
            else:
                msg += "\n"
            data = view_data[msg_id]
            receiver =  data['user_id']
>>>>>>> 7ed4c83cc6c4b71777347678a9f6ac79193cef25:userge/plugins/inline/secret.py
            msg += data['msg']
            u_id = c_q.from_user.id 
            if u_id == Config.OWNER_ID or u_id == receiver:
                await c_q.answer(msg, show_alert=True)
            else:
                await c_q.answer("This Message is Confidential 👽", show_alert=True)
        else:
<<<<<<< HEAD:userge/plugins/Satır İçi/secret.py
            await callback_query.answer("Hey, Bekle! Bu mesaj aşırı gizlidir 👽", show_alert=True)
||||||| e151c67:userge/plugins/inline/secret.py
            await callback_query.answer("This Message is Confidential 👽", show_alert=True)
=======
            await c_q.answer("𝘛𝘩𝘪𝘴 𝘮𝘦𝘴𝘴𝘢𝘨𝘦 𝘥𝘰𝘦𝘴𝘯'𝘵 𝘦𝘹𝘪𝘴𝘵 𝘢𝘯𝘺𝘮𝘰𝘳𝘦.", show_alert=True)

>>>>>>> 7ed4c83cc6c4b71777347678a9f6ac79193cef25:userge/plugins/inline/secret.py

@userge.on_cmd("secret", about={
    'header': "yardım için .secret yazın"})
async def secret_(message: Message):
    text = "**YANLIZCA SATIR İÇİ !**\n\n"
    text += "@botunuzunadi secret [kullanıcıadı VEYA kullanıcıid]  \"Gizli mesajın\""
    await message.edit(text, del_in=20)
    