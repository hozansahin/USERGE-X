# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.

from userge import userge, Message


@userge.on_cmd("json", about={
    'header': "gönderilen mesajı json'a çevir",
    'usage': "herhangi bir mesaja {tr}json yaz"})
async def jsonify(message: Message):
    msg = str(message.reply_to_message) if message.reply_to_message else str(message)
    await message.edit_or_send_as_file(text=msg, filename="json.txt", caption="Too Large")
