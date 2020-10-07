""" Son Sticker Bükücü """

# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.

import io
import os
import random
import emoji

import aiohttp
from PIL import Image
from pyrogram.raw.functions.messages import GetStickerSet
from pyrogram.raw.types import InputStickerSetShortName
from pyrogram.errors.exceptions.bad_request_400 import YouBlockedUser

from userge import userge, Message, Config


@userge.on_cmd(
    "kang", about={
        'header': "Stikır çıkartmaları dızlar 🤠",
        'usage': "Bir çıkartmaya {tr}kang [emoji (ler)] [paket numarası] yazın veya  "
                 "fotoğraf göndermen gerek!",
        'examples': ["{tr}kang", "{tr}kang 🤔", "{tr}kang 2", "{tr}kang 🤠 2"]},
    allow_channels=False, allow_via_bot=False)
async def kang_(message: Message):
    """ Stikır dızla """
    user = await userge.get_me()
    replied = message.reply_to_message
    photo = None
    emoji_ = None
    is_anim = False
    resize = False
    if replied and replied.media:
        if replied.photo:
            resize = True
        elif replied.document and "image" in replied.document.mime_type:
            resize = True
        elif replied.document and "tgsticker" in replied.document.mime_type:
            is_anim = True
        elif replied.sticker:
            if not replied.sticker.file_name:
                await message.edit("`Çıkartmanın adı yok!`")
                return
            emoji_ = replied.sticker.emoji
            is_anim = replied.sticker.is_animated
            if not replied.sticker.file_name.endswith('.tgs'):
                resize = True
        else:
            await message.edit("`Desteklenmeyen dosya!`")
            return
        await message.edit(f"`{random.choice(KANGING_STR)}`")
        photo = await userge.download_media(message=replied,
                                            file_name=Config.DOWN_PATH)
    else:
        await message.edit("`Bunu Dızlayamam...`")
        return
    if photo:
        args = message.input_str.split()
        pack = 1
        if len(args) == 2:
            emoji_, pack = args
        elif len(args) == 1:
            if args[0].isnumeric():
                pack = int(args[0])
            else:
                emoji_ = args[0]

        if emoji_ and emoji_ not in emoji.UNICODE_EMOJI:
            emoji_ = None
        if not emoji_:
            emoji_ = "🤔"

        u_name = user.username
        u_name = "@" + u_name if u_name else user.first_name or user.id
        packname = f"a{user.id}_by_userge_{pack}"
        custom_packnick = Config.CUSTOM_PACK_NAME or f"{u_name}'s kang pack"
        packnick = f"{custom_packnick} Vol.{pack}"
        cmd = '/newpack'
        if resize:
            photo = resize_photo(photo)
        if is_anim:
            packname += "_anim"
            packnick += " (Animated)"
            cmd = '/newanimated'
        async with aiohttp.ClientSession() as ses:
            async with ses.get(f'http://t.me/addstickers/{packname}') as res:
                htmlstr = (await res.text()).split('\n')
        if ("  A <strong>Telegram</strong> user has created "
                "the <strong>Sticker&nbsp;Set</strong>.") not in htmlstr:
            async with userge.conversation('Stickers', limit=30) as conv:
                try:
                    await conv.send_message('/addsticker')
                except YouBlockedUser:
                    await message.edit('first **unblock** @Stickers')
                    return
                await conv.get_response(mark_read=True)
                await conv.send_message(packname)
                msg = await conv.get_response(mark_read=True)
                limit = "50" if is_anim else "120"
                while limit in msg.text:
                    pack += 1
                    packname = f"a{user.id}_by_userge_{pack}"
                    packnick = f"{custom_packnick} Vol.{pack}"
                    if is_anim:
                        packname += "_anim"
                        packnick += " (Animated)"
                    await message.edit("`Switching to Pack " + str(pack) +
                                       " due to insufficient space`")
                    await conv.send_message(packname)
                    msg = await conv.get_response(mark_read=True)
                    if msg.text == "Invalid pack selected.":
                        await conv.send_message(cmd)
                        await conv.get_response(mark_read=True)
                        await conv.send_message(packnick)
                        await conv.get_response(mark_read=True)
                        await conv.send_document(photo)
                        await conv.get_response(mark_read=True)
                        await conv.send_message(emoji_)
                        await conv.get_response(mark_read=True)
                        await conv.send_message("/publish")
                        if is_anim:
                            await conv.get_response(mark_read=True)
                            await conv.send_message(f"<{packnick}>")
                        await conv.get_response(mark_read=True)
                        await conv.send_message("/skip")
                        await conv.get_response(mark_read=True)
                        await conv.send_message(packname)
                        await conv.get_response(mark_read=True)
                        await message.edit(
                            f"`Sticker added in a Different Pack !\n"
                            "This Pack is Newly created!\n"
                            f"Your pack can be found [here](t.me/addstickers/{packname})")
                        return
                await conv.send_document(photo)
                rsp = await conv.get_response(mark_read=True)
                if "Sorry, the file type is invalid." in rsp.text:
                    await message.edit("`Failed to add sticker, use` @Stickers "
                                       "`bot to add the sticker manually.`")
                    return
                await conv.send_message(emoji_)
                await conv.get_response(mark_read=True)
                await conv.send_message('/done')
                await conv.get_response(mark_read=True)
        else:
            await message.edit("`Brewing a new Pack...`")
            async with userge.conversation('Stickers') as conv:
                try:
                    await conv.send_message(cmd)
                except YouBlockedUser:
                    await message.edit('first **unblock** @Stickers')
                    return
                await conv.get_response(mark_read=True)
                await conv.send_message(packnick)
                await conv.get_response(mark_read=True)
                await conv.send_document(photo)
                rsp = await conv.get_response(mark_read=True)
                if "Sorry, the file type is invalid." in rsp.text:
                    await message.edit("`Failed to add sticker, use` @Stickers "
                                       "`bot to add the sticker manually.`")
                    return
                await conv.send_message(emoji_)
                await conv.get_response(mark_read=True)
                await conv.send_message("/publish")
                if is_anim:
                    await conv.get_response(mark_read=True)
                    await conv.send_message(f"<{packnick}>")
                await conv.get_response(mark_read=True)
                await conv.send_message("/skip")
                await conv.get_response(mark_read=True)
                await conv.send_message(packname)
                await conv.get_response(mark_read=True)
        await message.edit(f"**Stikır dızlandı** [Burada](t.me/addstickers/{packname}) **Bulabilirsin!**")
        if os.path.exists(str(photo)):
            os.remove(photo)


@userge.on_cmd("stkrinfo", about={
    'header': "çıkartma paket bilgisini al",
    'usage': "herhangi bir çıkartmaya {tr}stkrinfo yazın"})
async def sticker_pack_info_(message: Message):
    """ çıkartma paket bilgisini al """
    replied = message.reply_to_message
    if not replied:
        await message.edit("`Hiçbir şeyden bilgi alamıyorum, değil mi?`")
        return
    if not replied.sticker:
        await message.edit("`Paket bilgisini almak için bir çıkartmayı yanıtlayın`")
        return
    await message.edit("`Çıkartma paketinin bilgisi alınıyor, lütfen bekleyin ..`")
    get_stickerset = await message.client.send(
        GetStickerSet(
            stickerset=InputStickerSetShortName(
                short_name=replied.sticker.set_name)))
    pack_emojis = []
    for document_sticker in get_stickerset.packs:
        if document_sticker.emoticon not in pack_emojis:
            pack_emojis.append(document_sticker.emoticon)
    out_str = f"** paket adı:** `{get_stickerset.set.title}\n`" \
        f"**Stikır Kısa Adı:** `{get_stickerset.set.short_name}`\n" \
        f"**Arşivlendi mi?:** `{get_stickerset.set.archived}`\n" \
        f"**Resmi:** `{get_stickerset.set.official}`\n" \
        f"**Maskeler:** `{get_stickerset.set.masks}`\n" \
        f"**Animasyonlu mu?:** `{get_stickerset.set.animated}`\n" \
        f"**Paketteki Çıkartma sayısı:** `{get_stickerset.set.count}`\n" \
        f"**Paketteki Emojiler:**\n{' '.join(pack_emojis)}"
    await message.edit(out_str)


def resize_photo(photo: str) -> io.BytesIO:
    """ Resize the given photo to 512x512 """
    image = Image.open(photo)
    maxsize = 512
    scale = maxsize / max(image.width, image.height)
    new_size = (int(image.width*scale), int(image.height*scale))
    image = image.resize(new_size, Image.LANCZOS)
    resized_photo = io.BytesIO()
    resized_photo.name = "sticker.png"
    image.save(resized_photo, "PNG")
    os.remove(photo)
    return resized_photo


KANGING_STR = (
    "Çıkartmayı dızlıyorum...",
    "Yaşasın dızcılık...",
    "Bu çıkartmayı kendi paketime davet ediyorum...",
    "Bunu dızlamam lazım...",
    "Hey bu güzel bir çıkartma!\nHemen dızlıyorum..",
    "Çıkartmanı dızlıyorum\nhahaha.",
    "Hey şuraya bak. (☉｡☉)!→\nBen bunu dızlarken...",
    "Güller kırmızı menekşeler mavi, bu çıkartmayı paketime dızlayarak havalı olacağım...",
    "Çıkartma hapsediliyor...",
    "Bay dızcı bu çıkartmayı dızlıyor... ")