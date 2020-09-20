""" metin yapıştırma servisi """

# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.

import os

import aiohttp
from aiohttp import ClientResponseError, ServerTimeoutError, TooManyRedirects

from userge import userge, Message, Config

DOGBIN_URL = "https://del.dog/"
NEKOBIN_URL = "https://nekobin.com/"


@userge.on_cmd("paste", about={
    'header': "Metin veya metin dosyasını yapıştırma servislerine gönderir",
    'flags': {'-n': "nekobin kullan"},
    'usage': "{tr}paste [parametre] [file_type] [text | reply to msg]",
    'examples': "{tr}paste -py import os"}, del_pre=True)
async def paste_(message: Message) -> None:
    """metni doğrudan dogbin veya nekobin servislerine yapıştırır """
    await message.edit("`İşleniyor...`")
    text = message.filtered_input_str
    replied = message.reply_to_message
    use_neko = False
    file_ext = '.txt'
    if not text and replied:
        if replied.document and replied.document.file_size < 2 ** 20 * 10:
            file_ext = os.path.splitext(replied.document.file_name)[1]
            path = await replied.download(Config.DOWN_PATH)
            with open(path, 'r') as d_f:
                text = d_f.read()
            os.remove(path)
        elif replied.text:
            text = replied.text
    if not text:
        await message.err("Veri bulunamadı!")
        return
    flags = list(message.flags)
    if 'n' in flags:
        use_neko = True
        flags.remove('n')
    if flags and len(flags) == 1:
        file_ext = '.' + flags[0]
    await message.edit("`Metni yapıştırıyorum ...`")
    async with aiohttp.ClientSession() as ses:
        if use_neko:
            async with ses.post(NEKOBIN_URL + "api/documents", json={"content": text}) as resp:
                if resp.status == 201:
                    response = await resp.json()
                    key = response['result']['key']
                    final_url = NEKOBIN_URL + key + file_ext
                    reply_text = f"**Nekobin** [URL]({final_url})"
                    await message.edit(reply_text, disable_web_page_preview=True)
                else:
                    await message.err("Nekobin'e ulaşılamadı")
        else:
            async with ses.post(DOGBIN_URL + "documents", data=text.encode('utf-8')) as resp:
                if resp.status == 200:
                    response = await resp.json()
                    key = response['key']
                    final_url = DOGBIN_URL + key
                    if response['isUrl']:
                        reply_text = (f"**Kısa** [URL]({final_url})\n"
                                      f"**Dogbin** [URL]({DOGBIN_URL}v/{key})")
                    else:
                        reply_text = f"**Dogbin** [URL]({final_url}{file_ext})"
                    await message.edit(reply_text, disable_web_page_preview=True)
                else:
                    await message.err("Dogbin'e ulaşılamadı")


@userge.on_cmd("getpaste", about={
    'header': "Bir yapıştırma servisinin içeriğini alır",
    'usage': "{tr}getpaste [del.dog or nekobin link]"})
async def get_paste_(message: Message):
    """ dogbin veya nekobin URL'sinin içeriğini getirir """
    link = message.input_str
    if not link:
        await message.err("veri girişi bulunamadı!")
        return
    await message.edit("`Yapıştırılmış içerik alınıyor ...`")
    format_view = f'{DOGBIN_URL}v/'
    if link.startswith(format_view):
        link = link[len(format_view):]
        raw_link = f'{DOGBIN_URL}raw/{link}'
    elif link.startswith(DOGBIN_URL):
        link = link[len(DOGBIN_URL):]
        raw_link = f'{DOGBIN_URL}raw/{link}'
    elif link.startswith("del.dog/"):
        link = link[len("del.dog/"):]
        raw_link = f'{DOGBIN_URL}raw/{link}'
    elif link.startswith(NEKOBIN_URL):
        link = link[len(NEKOBIN_URL):]
        raw_link = f'{NEKOBIN_URL}raw/{link}'
    elif link.startswith("nekobin.com/"):
        link = link[len("nekobin.com/"):]
        raw_link = f'{NEKOBIN_URL}raw/{link}'
    else:
        await message.err("Bu bir yapıştırma servisi URL'si mi?")
        return
    async with aiohttp.ClientSession(raise_for_status=True) as ses:
        try:
            async with ses.get(raw_link) as resp:
                text = await resp.text()
        except ServerTimeoutError as e_r:
            await message.err(f"İstek zaman aşımına uğradı -> {e_r}")
        except TooManyRedirects as e_r:
            await message.err("Hatalı İstek "
                              f"maksimum yönlendirme sayısı -> {e_r}")
        except ClientResponseError as e_r:
            await message.err(f"İstek, başarısız bir hata kodu döndürdü -> {e_r}")
        else:
            await message.edit_or_send_as_file("--İçerik Başarıyla Getirildi !--"
                                               f"\n\n**İşte! içerik** :\n`{text}`")
