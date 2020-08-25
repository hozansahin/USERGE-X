from userge import userge, Config, get_collection, Message
from pyrogram import Filters, CallbackQuery
SECRET_MSG = get_collection("SECRET_MSG") 


if Config.BOT_TOKEN and Config.OWNER_ID:
    if Config.HU_STRING_SESSION:
        ubot = userge.bot
    else:
        ubot = userge

       
    @ubot.on_callback_query(filters=Filters.regex(pattern=r"^secret_btn$"))
    async def alive_callback(_, callback_query: CallbackQuery): 
        sender = await userge.get_me()
        msg = f"🔓 **{sender.first_name}** : tarafından gelen mesaj "
        if sender.last_name:
            msg += f" {sender.last_name}\n"
        else:
            msg += "\n"
        async for data in SECRET_MSG.find():
            receiver = data['user_id']
            msg += data['msg']
        u_id = callback_query.from_user.id 
        if u_id == Config.OWNER_ID or u_id == receiver:
            await callback_query.answer(msg, show_alert=True)
        else:
            await callback_query.answer("Hey, Bekle! Bu mesaj aşırı gizlidir 👽", show_alert=True)

@userge.on_cmd("secret", about={
    'header': "Satır İçi Bot ile Gizli Mesaj Göndermenize yarar"})
async def secret_(message: Message):
    text = "**YANLIZCA SATIR İÇİ !**\n\n"
    text += "@botunuzunadi secret @behsedilen <Gizli mesajın>"
    await message.edit(text, del_in=10)
    