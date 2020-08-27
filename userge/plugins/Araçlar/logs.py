# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.

from userge import userge, Message, logging, Config, pool
import os
import aiohttp

NEKOBIN_URL = "https://nekobin.com/"
NEKOBIN_URL_RAW = "https://nekobin.com/raw/"

_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}


@userge.on_cmd("logs", about={
    'header': "USERGE-X Loglarını kontrol edin",
    'flags': {
        '-h': "heroku Loglarını getir",
        '-l': "heroku Log satırı sınırı: varsayılan 100"}}, allow_channels=False)
async def check_logs(message: Message):
    """ Logları kontrol et """
    await message.edit("`Loglar kontrol ediliyor ...`")
    if '-h' in message.flags and Config.HEROKU_APP:
        limit = int(message.flags.get('-l', 100))
        logs = await pool.run_in_thread(Config.HEROKU_APP.get_log)(lines=limit)
        await message.client.send_as_file(chat_id=message.chat.id,
                                          text=logs,
                                          filename='userge-heroku.log',
                                          caption=f'userge-heroku.log [ {limit} lines ]')
    else:
        with open("logs/userge.log", 'r') as d_f:
            text = d_f.read()
        file_ext = '.txt'
        async with aiohttp.ClientSession() as ses:
            async with ses.post(NEKOBIN_URL + "api/documents", json={"content": text}) as resp:
                if resp.status == 201:
                    response = await resp.json()
                    key = response['result']['key']
                    final_url = NEKOBIN_URL + key + file_ext
                    final_url_raw = NEKOBIN_URL_RAW + key + file_ext
                    reply_text = "**İşte USERGE-X Logları** - \n"
                    reply_text += f"• [Neko]({final_url})\n"
                    reply_text += f"• [Neko_RAW]({final_url_raw})"
                    await message.edit(reply_text, disable_web_page_preview=True)
                else:
                    await message.err("Nekobin'e ulaşılamadı..")
        


@userge.on_cmd("setlvl", about={
    'header': "Logların seviyesini ayarla, varsayılan olarak info",
    'types': ['debug', 'info', 'warning', 'error', 'critical'],
    'usage': "{tr}setlvl [level]",
    'examples': ["{tr}setlvl info", "{tr}setlvl debug"]})
async def set_level(message: Message):
    """ Log seviyesini ayarlar"""
    await message.edit("`Log seviyesi ayarlanıyor ...`")
    level = message.input_str.lower()
    if level not in _LEVELS:
        await message.err("bilinmeyen seviye!")
        return
    for logger in (logging.getLogger(name) for name in logging.root.manager.loggerDict):
        logger.setLevel(_LEVELS[level])
    await message.edit(f"**{level.upper()}** : `Log seviyesine başarıyla ayarlandı`", del_in=3)
