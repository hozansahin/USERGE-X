from userge import userge, Message, Config
from pyrogram.types import (  
     InlineKeyboardMarkup, InlineKeyboardButton) #CallbackQuery
from pyrogram import filters
from pyrogram.errors.exceptions import FileIdInvalid, FileReferenceEmpty
from pyrogram.errors.exceptions.bad_request_400 import BadRequest

# https://github.com/UsergeTeam/Userge-Assistant/.../alive.py#L41
# refresh file id and file reference from TG server

LOGO_ID, LOGO_REF = None, None


if Config.BOT_TOKEN and Config.OWNER_ID:
    if Config.HU_STRING_SESSION:
        ubot = userge.bot
    else:
        ubot = userge


    @ubot.on_message(filters.private & filters.command("start"))
    async def start_bot(_, message: Message):
        bot = await userge.bot.get_me()
        master = await userge.get_me()
        hello = f"""
Merhaba [{message.from_user.first_name}](tg://user?id={message.from_user.id})",
Tanıştığıma memnun oldum! Ben **@{bot.username}**

      **USERGE-X**  Tarafından Desteklenen Bir Botum

**{master.first_name}** - <i> Sahibimle İletişime Geçebilirsiniz.</i>
<i>Ve Daha Fazla Bilgi İçin Repo'yu Kontrol Edin</i>
"""
        u_n = master.username
        try:
            if LOGO_ID:
                await sendit(message, LOGO_ID, LOGO_REF, hello, u_n)
            else:
                await refresh_id()
                await sendit(message, LOGO_ID, LOGO_REF, hello, u_n)
        except (FileIdInvalid, FileReferenceEmpty, BadRequest):
            await refresh_id()
            await sendit(message, LOGO_ID, LOGO_REF, hello, u_n)


    async def refresh_id():
        global LOGO_ID, LOGO_REF
        vid = (await ubot.get_messages('Errors_Archive', 8826)).video
        LOGO_ID = vid.file_id
        LOGO_REF = vid.file_ref


    async def sendit(message, fileid, fileref, caption, u_n):
        await ubot.send_video(
            chat_id=message.chat.id,
            video=fileid, 
            file_ref=fileref,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("İLETİŞİM", url=f"t.me/{u_n}"),
                InlineKeyboardButton("REPO", url="https://github.com/code-rgb/USERGE-X")
                ]]
            )
        )


@userge.on_cmd("bot_pm", about={
    'header': "Botunuzun /start komutuna yanıt vermesini sağlayan modül"})
async def op_(message: Message):
    text = "**Sadece BOT'un PM'sinde çalışır**\n\n"
    text += "<code>kullanmak için botunuza /start yazın</code>"
    await message.edit(text, del_in=20)
