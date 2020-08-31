# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.

from json import dumps
from emoji import get_emoji_regexp

from googletrans import Translator, LANGUAGES

from userge import userge, Message, Config


@userge.on_cmd("tr", about={
    'header': "Google Translate'i kullanarak verilen metni çevir",
    'supported languages': dumps(LANGUAGES, indent=4, sort_keys=True),
    'usage': "İngilizce'den türkçe'ye\n"
             "{tr}tr -en -tr i am userge\n\n"
             "otomatik olarak algılanan dilden türkçe'ye\n"
             "{tr}tr -tr i am userge\n\n"
             "otomatik algılanan dilden varsayılan dile \n"
             "{tr}tr i am userge\n\n"
             "İngilizce'den türkçe'ye çevirmek istediğiniz mesaja cevap verin\n"
             "{tr}tr -en -tr\n\n"
             "otomatik algılanan dilden türkçe'ye çevirmek istediğiniz mesajı yanıtlayın\n"
             "{tr}tr -tr\n\n"
             "otomatik olarak algılanan dilden tercih edilen dile çevirmek istediğiniz mesajı yanıtlayın\n"
             "{tr}tr"}, del_pre=True)
async def translateme(message: Message):
    translator = Translator()
    text = message.filtered_input_str
    flags = message.flags
    if message.reply_to_message:
        text = message.reply_to_message.text
    if not text:
        await message.err(
            text="Çevirmek için bir mesaja veya bir metine cevap verin!\nyardım için `.help tr`")
        return
    if len(flags) == 2:
        src, dest = list(flags)
    elif len(flags) == 1:
        src, dest = 'auto', list(flags)[0]
    else:
        src, dest = 'auto', Config.LANG
    text = get_emoji_regexp().sub(u'', text)
    await message.edit("Çeviriyorum...")
    try:
        reply_text = translator.translate(
            text, dest=dest, src=src)
    except ValueError:
        await message.err(text="Geçersiz hedef dil.\nyardım için `.help tr`")
        return
    source_lan = LANGUAGES[f'{reply_text.src.lower()}']
    transl_lan = LANGUAGES[f'{reply_text.dest.lower()}']
    output = f"**Kaynak dil ({source_lan.title()}):**`\n{text}`\n\n\
**Çevrilen dil ({transl_lan.title()}):**\n`{reply_text.text}`"
    await message.edit_or_send_as_file(text=output, caption="translated")
