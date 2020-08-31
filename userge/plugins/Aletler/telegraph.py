# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.

import os

from telegraph import upload_file

from userge import userge, Message, Config
from userge.utils import progress

_T_LIMIT = 5242880


@userge.on_cmd("telegraph", about={
    'header': "Telegra.ph sunucularına dosya yükleyin",
    'types': ['.jpg', '.jpeg', '.png', '.gif', '.mp4'],
    'usage': "{tr}telegraph desteklenen medyaya göre yanıtla: 5MB ile sınırlıdır"})
async def telegraph_(message: Message):
    replied = message.reply_to_message
    if not replied:
        await message.err("desteklenen medyayı yanıtla")
        return
    if not ((replied.photo and replied.photo.file_size <= _T_LIMIT)
            or (replied.animation and replied.animation.file_size <= _T_LIMIT)
            or (replied.video and replied.video.file_name.endswith('.mp4')
                and replied.video.file_size <= _T_LIMIT)
            or (replied.document
                and replied.document.file_name.endswith(
                    ('.jpg', '.jpeg', '.png', '.gif', '.mp4'))
                and replied.document.file_size <= _T_LIMIT)):
        await message.err("desteklenmiyor!")
        return
    await message.edit("`işleniyor...`")
    dl_loc = await message.client.download_media(
        message=message.reply_to_message,
        file_name=Config.DOWN_PATH,
        progress=progress,
        progress_args=(message, "indirmeye çalışıyor")
    )
    await message.edit("`telegraph'a yükleniyor...`")
    try:
        response = upload_file(dl_loc)
    except Exception as t_e:
        await message.err(t_e)
    else:
        await message.edit(f"**[İşte Telegra.ph Bağlantınız!](https://telegra.ph{response[0]})**")
    finally:
        os.remove(dl_loc)
