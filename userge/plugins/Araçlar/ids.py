# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.

from userge import userge, Message


@userge.on_cmd("ids", about={
    'header': "idleri görüntüle",
    'usage': "{tr}ids herhangi bir mesaja veya dosya'ya bu komutu gönderin"})
async def getids(message: Message):
    msg = message.reply_to_message or message
    out_str = f"👥 **Chat ID** : `{(msg.forward_from_chat or msg.chat).id}`\n"
    out_str += f"💬 **Mesaj ID** : `{msg.forward_from_message_id or msg.message_id}`\n"
    if msg.from_user:
        out_str += f"🙋‍♂️ **Kullanıcı ID** : `{msg.from_user.id}`\n"
    file_id = None
    if msg.audio:
        type_ = "müzik"
        file_id = msg.audio.file_id
    elif msg.animation:
        type_ = "animasyon"
        file_id = msg.animation.file_id
    elif msg.document:
        type_ = "belge"
        file_id = msg.document.file_id
    elif msg.photo:
        type_ = "resim"
        file_id = msg.photo.file_id
    elif msg.sticker:
        type_ = "stiker"
        file_id = msg.sticker.file_id
    elif msg.voice:
        type_ = "ses kaydı"
        file_id = msg.voice.file_id
    elif msg.video_note:
        type_ = "video_note"
        file_id = msg.video_note.file_id
    elif msg.video:
        type_ = "video"
        file_id = msg.video.file_id
    if file_id is not None:
        out_str += f"📄 **Dosya ID** (`{type_}`): `{file_id}`"
    await message.edit(out_str)
