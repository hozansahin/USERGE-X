# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.

from userge import userge, Message


@userge.on_cmd("s", about={
    'header': "USERGE komutlarında arayın",
    'examples': "{tr}s wel"}, allow_channels=False)
async def search(message: Message):
    cmd = message.input_str
    if not cmd:
        await message.err(text="Komutlarda arama yapmak için herhangi bir anahtar kelime girin")
        return
    found = [i for i in sorted(list(userge.manager.enabled_commands)) if cmd in i]
    out_str = '    '.join(found)
    if found:
        out = f"** `{cmd}` : --için ({len(found)}) komut buldum--**\n\n`{out_str}`"
    else:
        out = f"`{cmd}`: __için komut bulunamadı__  "
    await message.edit(text=out, del_in=0)
