from userge import userge, Message, Config, get_collection
from pyrogram.types import (  
     InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery )
from pyrogram import filters
from pyrogram.errors.exceptions import FileIdInvalid, FileReferenceEmpty
from pyrogram.errors.exceptions.bad_request_400 import BadRequest
from datetime import date
import asyncio


BOT_START = get_collection("BOT_START")

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
        u_id = message.from_user.id
        f_name = message.from_user.first_name
        hello = f"""
Merhaba [{f_name}](tg://user?id={u_id}),
Tanıştığıma memnun oldum! Ben **@{bot.username}**

      **USERGE-X**  Tarafından Desteklenen Bir Botum

**{master.first_name}** - <i> Sahibimle İletişime Geçebilirsiniz.</i>
<i>Ve Daha Fazla Bilgi İçin Repo'yu Kontrol Edin</i>
"""
        if u_id != Config.OWNER_ID:
            found = await BOT_START.find_one({'user_id': u_id})
            if not found:
                today = date.today()
                d2 = today.strftime("%B %d, %Y")
                start_date = d2.replace(',', '')
                u_n = master.username
                await asyncio.gather(
                    BOT_START.insert_one(
                        {'firstname': f_name, 'user_id': u_id, 'date': start_date}))
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
        vid = (await ubot.get_messages('useless_x', 2)).video
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
                InlineKeyboardButton("REPO", url="https://github.com/code-rgb/USERGE-X")],
                [InlineKeyboardButton("➕ GRUBA EKLE", callback_data="add_to_grp")
                ]]
            )
        )


    @ubot.on_callback_query(filters.regex(pattern=r"^add_to_grp$"))
    async def add_to_grp(_, callback_query: CallbackQuery): 
        u_id = callback_query.from_user.id 
        if u_id == Config.OWNER_ID:
            botname = (await ubot.get_me()).username
            msg = "**🤖 Botunuzu gruba ekleyin** \n\n <u>Note:</u>  <i>Yönetici Yetkileri Gerekli !</i>"
            add_bot = f"http://t.me/{botname}?startgroup=start"

            buttons = [[InlineKeyboardButton("➕ EKLEMEK İÇİN TIKLAYIN", url=add_bot)]]
            await callback_query.edit_message_text(
                    msg,
                    reply_markup=InlineKeyboardMarkup(buttons)
            )
        else:
            await callback_query.answer("BUNU SADECE SAHİBİM YAPABİLİR !\n\nKendi userge-x botunuzu kurun !", show_alert=True)
 
 
@userge.on_cmd("bot_pm", about={
    'header': "Botunuzun /start komutuna yanıt vermesini sağlayan modül"})
async def op_(message: Message):
    text = "**Sadece BOT'un PM'sinde çalışır**\n\n"
    text += "<code>kullanmak için botunuza /start yazın</code>"
    await message.edit(text, del_in=20)


@userge.on_cmd("startlist", about={
    'header': "BOT'nuzu başlatan, yani Bot PM'de /start yazan Kullanıcıların Geçmişini Alın",
    'examples': "{tr}startlist"},
    allow_channels=False)
async def start_list(message: Message):
    msg = ""      
    async for c in BOT_START.find():  
        msg += f"• <i>ID:</i> <code>{c['user_id']}</code>\n    <b>İsim:</b> {c['firstname']},  <b>Tarih:</b> `{c['date']}`\n"
    await message.edit_or_send_as_file(
        f"<u><i><b> Bot PM geçmişi</b></i></u>\n\n{msg}" if msg else "`Kimse daha iyisini yapamaz`")




