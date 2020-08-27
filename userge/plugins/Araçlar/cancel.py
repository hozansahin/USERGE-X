# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.

from userge import userge, Message


@userge.on_cmd("cancel", about={'header': "İptal Etmek İstediğiniz Mesaj için kullanılır"})
async def cancel_(message: Message):
    replied = message.reply_to_message
    if replied:
        replied.cancel_the_process()
        await message.edit(
            "`iptal listesine ekledi`", del_in=5)
    else:
        await message.edit(
            "`iptal etmek istediğiniz mesaja yazın`", del_in=5)
