# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.

import os
import wget
import speedtest
from userge import userge, Message
from userge.utils import humanbytes

CHANNEL = userge.getCLogger(__name__)


@userge.on_cmd("speedtest", about={'header': "Sunucu Hızınızı Test Edin"})
async def speedtst(message: Message):
    await message.edit("`hızı testi yapılıyor. . .`")
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        await message.try_to_edit("`İndirme hızı ölçülüyor . . .`")
        test.download()
        await message.try_to_edit("`Yükleme hızı ölçülüyor . . .`")
        test.upload()
        test.results.share()
        result = test.results.dict()
    except Exception as e:
        await message.err(text=e)
        return
    path = wget.download(result['share'])
    output = f"""**--{result['timestamp']} Anlık Test --

İstemci:

Sağlayıcı: `{result['client']['isp']}`
Ülke Kısaltması: `{result['client']['country']}`

Sunucu:

Konum: `{result['server']['name']}`
Ülke: `{result['server']['country']}, {result['server']['cc']}`
Sponsor: `{result['server']['sponsor']}`
Tepki: `{result['server']['latency']}`

Ping: `{result['ping']}`
Gönderilen: `{humanbytes(result['bytes_sent'])}`
Alınan: `{humanbytes(result['bytes_received'])}`
İndirme: `{humanbytes(result['download'] / 8)}/s`
Yükleme: `{humanbytes(result['upload'] / 8)}/s`**"""
    msg = await message.client.send_photo(chat_id=message.chat.id,
                                          photo=path,
                                          caption=output)
    await CHANNEL.fwd_msg(msg)
    os.remove(path)
    await message.delete()
