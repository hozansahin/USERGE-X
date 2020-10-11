# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.

from datetime import datetime

from userge import userge, Message


@userge.on_cmd("purge", about={
    'header': "Kullanıcı mesajlarını temizleme",
    'flags': {
        '-u': "cevaplanan mesajdan user_id alır",
        '-l': "Maksimum mesaj sınırı:  100"},
    'usage': "temizlemek istediğiniz mesaja {tr}purge yazın.\n"
             "{tr}purge [user_id | user_name] kullanıcısından gelen mesajları temizlemek için parametre kullanımı",
    'examples': ['{tr}purge', '{tr}purge -u', '{tr}purge [user_id | user_name]']},
    allow_bots=False, del_pre=True)
async def purge_(message: Message):
    await message.edit("`Siliyorum ...`")
    from_user_id = None
    if message.filtered_input_str:
        from_user_id = (await message.client.get_users(message.filtered_input_str)).id
    start_message = 0
    if 'l' in message.flags:
        limit = int(message.flags['l'])
        if limit > 100:
            limit = 100
        start_message = message.message_id - limit
    if message.reply_to_message:
        start_message = message.reply_to_message.message_id
        if 'u' in message.flags:
            from_user_id = message.reply_to_message.from_user.id
    if not start_message:
        await message.err("Nereden Başlayacağımı belirtmelisin")
        return
    start_t = datetime.now()
    # message_ids = range(start_message, message.message_id)
    list_of_messages = []
    purged_messages_count = 0
    async for a_message in message.client.iter_history(
            chat_id=message.chat.id, limit=None,
            offset_id=start_message, reverse=True):
        if (from_user_id and a_message and a_message.from_user
                and a_message.from_user.id == from_user_id):
            list_of_messages.append(a_message.message_id)
        if not from_user_id:
            list_of_messages.append(a_message.message_id)
        if len(list_of_messages) >= 100:
            await message.client.delete_messages(
                chat_id=message.chat.id,
                message_ids=list_of_messages
            )
            purged_messages_count += len(list_of_messages)
            list_of_messages = []
    if list_of_messages:
        await message.client.delete_messages(chat_id=message.chat.id,
                                             message_ids=list_of_messages)
        purged_messages_count += len(list_of_messages)
    end_t = datetime.now()
    time_taken_s = (end_t - start_t).seconds
    out = f"{purged_messages_count} Mesaj {time_taken_s} saniyede. <u>Temizlendi!</u> "
    await message.edit(out, del_in=3)