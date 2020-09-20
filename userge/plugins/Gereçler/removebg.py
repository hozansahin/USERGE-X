# Userge Plugin for removing background from Images
# Author: Sumanjay (https://github.com/cyberboysumanjay) (@cyberboysumanjay)
# All rights reserved.

import os
from datetime import datetime

from removebg import RemoveBg

from userge import userge, Config, Message
from userge.utils import progress

IMG_PATH = Config.DOWN_PATH + "dl_image.jpg"


@userge.on_cmd('removebg', about={
    'header': "Resimden Arka Planı Kaldırır (ücretsiz API'de Ayda 50 istek)",
    'usage': "{tr}removebg [herhangi bir fotoğrafı yanıtlayın | fotoğrafın bağlantısı]"})
async def remove_background(message: Message):
    if not Config.REMOVE_BG_API_KEY:
        await message.edit(
            "Apiyi<a href='https://www.remove.bg/b/background-removal-api'>Buradan Alın"
            "</a> & Heroku Config Vars'a <code>REMOVE_BG_API_KEY</code> ekleyin",
            disable_web_page_preview=True, parse_mode="html")
        return
    await message.edit("İnceliyorum...")
    replied = message.reply_to_message
    if (replied and replied.media
            and (replied.photo
                 or (replied.document and "image" in replied.document.mime_type))):
        start_t = datetime.now()
        if os.path.exists(IMG_PATH):
            os.remove(IMG_PATH)
        await message.client.download_media(message=replied,
                                            file_name=IMG_PATH,
                                            progress=progress,
                                            progress_args=(message, "Resim İndiriliyor"))
        end_t = datetime.now()
        m_s = (end_t - start_t).seconds
        await message.edit(f"Resim {m_s} saniye içinde kaydedildi. \n Arka Plan Şimdi Kaldırılıyor ...")
        # Cooking Image
        try:
            rmbg = RemoveBg(Config.REMOVE_BG_API_KEY, "removebg_error.log")
            rmbg.remove_background_from_img_file(IMG_PATH)
            rbg_img_path = IMG_PATH + "_no_bg.png"
            start_t = datetime.now()
            await message.client.send_document(
                chat_id=message.chat.id,
                document=rbg_img_path,
                disable_notification=True,
                progress=progress,
                progress_args=(message, "Yükleniyor", rbg_img_path))
            await message.delete()
        except Exception:
            await message.edit(" Bir şeyler ters gitti! \nkullanım kotanızı kontrol edin!")
            return
    else:
        await message.edit("Arka planı kaldırmak için bir resmi yanıtlayın!", del_in=5)
