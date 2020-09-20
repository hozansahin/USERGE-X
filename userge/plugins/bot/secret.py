# Copyright (C) 2020 BY - GitHub.com/code-rgb [TG - @deleteduser420]
# All rights reserved.

from userge import userge, Config, Message
from pyrogram.types import CallbackQuery
from pyrogram import filters
import json
import os

SECRETS = "userge/xcache/secret.txt"


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
            msg = f"🔓 {sender.first_name} ; Tarafından  1 gizli mesajın var ! "
            msg += f" {sender.last_name}\n" if sender.last_name else "\n"
            data = view_data[msg_id]
            receiver =  data['user_id']
            msg += data['msg']
            u_id = c_q.from_user.id
            if u_id in [Config.OWNER_ID, receiver]:
                await c_q.answer(msg, show_alert=True)
            else:
                await c_q.answer("Bu mesaj Çok Gizlidir!", show_alert=True)
        else:
            await c_q.answer("Bu mesaj artık mevcut değil", show_alert=True)

