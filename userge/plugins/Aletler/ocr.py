# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.

import os

import requests

from userge import userge, Message, Config, pool

CHANNEL = userge.getCLogger(__name__)


@pool.run_in_thread
def ocr_space_file(filename,
                   language='tur',
                   overlay=False,
                   api_key=Config.OCR_SPACE_API_KEY):
    """
    OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """
    payload = {
        'isOverlayRequired': overlay,
        'apikey': api_key,
        'language': language,
    }
    with open(filename, 'rb') as f:
        r = requests.post(
            'https://api.ocr.space/parse/image',
            files={filename: f},
            data=payload,
        )
    return r.json()


@userge.on_cmd("ocr", about={
    'header': "ocr okuyucuyu çalıştırmak için bunu kullanın",
    'description': "resimler için ocr(Okuma) sonucunu al (dosya boyutu sınırı = 1MB)",
    'examples': [
        "{tr}ocr [resmi yanıtla]",
        "{tr}ocr eng [resmi yanıtla] (Dil kodlarını 'https://ocr.space/ocrapi' burada bulabilirsin)"]})
async def ocr_gen(message: Message):
    """
    bu işlev görüntü dosyası için ocr(metin) çıktısı oluşturabilir
    """
    if Config.OCR_SPACE_API_KEY is None:
        await message.edit(
            "<code>Oops !! OCR API'sini şuradan alın</code> "
            "<a href='http://eepurl.com/bOLOcf'>TIKLA</a> "
            "<code>& Heroku config vars'a </code> (<code>OCR_SPACE_API_KEY</code>) Ekle",
            disable_web_page_preview=True,
            parse_mode="html", del_in=0)
        return

    if message.reply_to_message:

        lang_code = message.input_str if message.input_str else "eng"
        await message.edit(r"`Okumaya çalışıyorum...  📖")
        downloaded_file_name = await message.client.download_media(message.reply_to_message)
        test_file = await ocr_space_file(downloaded_file_name, lang_code)
        try:
            ParsedText = test_file["ParsedResults"][0]["ParsedText"]
        except Exception as e_f:
            await message.edit(
                r"`Okuyamadım.. (╯‵□′)╯︵┻━┻`"
                "\n`Sanırım yeni gözlüklere ihtiyacım var. 👓`"
                f"\n\n**HATA**: `{e_f}`", del_in=0)
            os.remove(downloaded_file_name)
            return
        else:
            await message.edit(
                "**İşte ondan okuyabileceklerim:**"
                f"\n\n`{ParsedText}`")
            os.remove(downloaded_file_name)
            await CHANNEL.log("`ocr` komut başarıyla çalıştırıldı")
            return

    else:
        await message.edit(r"`hiçbir şey okuyamıyorum (°ー°〃) , .help ocr yazın`", del_in=0)
        return
