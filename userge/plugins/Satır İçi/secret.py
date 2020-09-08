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
            msg += data['msg']
            u_id = c_q.from_user.id 
            if u_id == Config.OWNER_ID or u_id == receiver:
                await c_q.answer(msg, show_alert=True)
            else:
                await c_q.answer("Hey, Bekle! Bu mesaj aşırı gizlidir 👽", show_alert=True)
        else:
            await c_q.answer("bu mesaj artık Gözükmüyor.", show_alert=True)


@userge.on_cmd("secret", about={
    'header': "yardım için .secret yazın"})
async def secret_(message: Message):
    text = "**YANLIZCA SATIR İÇİ !**\n\n"
    text += "@botunuzunadi secret [kullanıcıadı VEYA kullanıcıid]  \"Gizli mesajın\""
    await message.edit(text, del_in=20)
    