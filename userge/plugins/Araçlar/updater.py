# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.

import asyncio

from git import Repo
from git.exc import GitCommandError

from userge import userge, Message, Config

LOG = userge.getLogger(__name__)
CHANNEL = userge.getCLogger(__name__)


@userge.on_cmd("update", about={
    'header': "Güncellemeleri Kontrol Et ve Botu Güncelle",
    'flags': {
        '-pull': "güncellemeleri getir",
        '-push': "güncellemeleri heroku'ya aktar",
        '-alpha': "alpha sürümü için al",
        '-develop': "Geliştirme sürümü için al"},
    'usage': "{tr}update : varsayılan güncellemeleri kontrol edin\n"
             "{tr}update -[sürüm] : herhangi bir sürüm için güncellemeleri kontrol edin\n"
             "güncellemeleri getirmek istiyorsan -pull Ekle\n"
             "herokuya güncellemeleri göndermek istiyorsanız -push ekleyin",
    'examples': "{tr}update -alpha -pull -push"}, del_pre=True, allow_channels=False)
async def check_update(message: Message):
    """ güncellemeleri kontrol et veya güncelle """
    await message.edit("`Güncellemeler kontrol ediliyor, lütfen bekleyin...`")
    repo = Repo()
    try:
        repo.remote(Config.UPSTREAM_REMOTE).fetch()
    except GitCommandError as error:
        await message.err(error, del_in=5)
        return
    flags = list(message.flags)
    pull_from_repo = False
    push_to_heroku = False
    branch = "master"
    if "pull" in flags:
        pull_from_repo = True
        flags.remove("pull")
    if "push" in flags:
        push_to_heroku = True
        flags.remove("push")
    if len(flags) == 1:
        branch = flags[0]
    if branch not in repo.branches:
        await message.err(f'{branch} :geçersiz parametre')
        return
    out = ''
    try:
        for i in repo.iter_commits(f'HEAD..{Config.UPSTREAM_REMOTE}/{branch}'):
            out += (f"🔨 **#{i.count()}** : "
                    f"[{i.summary}]({Config.UPSTREAM_REPO.rstrip('/')}/commit/{i}) "
                    f"👷 __{i.author}__\n\n")
    except GitCommandError as error:
        await message.err(error, del_in=5)
        return
    if out:
        if pull_from_repo:
            await message.edit(f'`[{branch}] İçin yeni güncelleme bulundu, Şimdi güncelleniyor ...`')
            await asyncio.sleep(1)
            repo.git.reset('--hard', 'FETCH_HEAD')
            await CHANNEL.log(f"**[{branch}] için  userge güncellemesi \n\n📄 YENİLİKLER 📄**\n\n{out}")
        elif not push_to_heroku:
            changelog_str = f'**[{branch}]: İçin yeni GÜNCELLEME mevcut \n\n📄 YENİLİKLER 📄**\n\n'
            await message.edit_or_send_as_file(changelog_str + out, disable_web_page_preview=True)
            return
    elif not push_to_heroku:
        await message.edit(f'**[{branch}] zaten güncel**', del_in=5)
        return
    if not push_to_heroku:
        await message.edit(
            '**Userge-x Başarıyla Güncellendi!**\n'
            '`Şimdi yeniden başlatılıyor... Lütfen Biraz bekle!', del_in=3)
        asyncio.get_event_loop().create_task(userge.restart(True))
        return
    if not Config.HEROKU_GIT_URL:
        await message.err("lütfen heroku değişkenlerini ayarlayın ...")
        return
    await message.edit(
        f'`[{branch}] sürümü için herokuya güncellemeler yapılıyor ...\n'
        'bu 5 dakika kadar sürecektir`\n\n'
        f'* 5 dakika sonra beni **yeniden başlat**\n Kullanım:  `{Config.CMD_TRIGGER}restart -h`\n\n'
        '*Yeniden başlatıldıktan sonra güncellemeleri tekrar kontrol edin :)')
    if "heroku" in repo.remotes:
        remote = repo.remote("heroku")
        remote.set_url(Config.HEROKU_GIT_URL)
    else:
        remote = repo.create_remote("heroku", Config.HEROKU_GIT_URL)
    remote.push(refspec=f'{branch}:master', force=True)
    await message.edit(f"**HEROKU ADI : {Config.HEROKU_APP.name}, [{branch}] sürümü için zaten güncel!**")
