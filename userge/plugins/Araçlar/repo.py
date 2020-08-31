# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.

from userge import userge, Message, Config


@userge.on_cmd("repo", about={'header': "repo URL'si ve kullanım klavuzu"})
async def see_repo(message: Message):
    """depoyu görüntüle"""
    output = f"• **repo** : [USERGE-X]({Config.UPSTREAM_REPO})"
    await message.edit(output)
