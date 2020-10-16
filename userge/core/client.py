# pylint: disable=missing-module-docstring
#
# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.

__all__ = ['Userge']

import time
import signal
import asyncio
import importlib
from types import ModuleType
from typing import List, Awaitable, Any, Optional, Union

from pyrogram import idle

from userge import logging, Config, logbot
from userge.utils import time_formatter
from userge.utils.exceptions import UsergeBotNotFound
from userge.plugins import get_all_plugins
from .methods import Methods
from .ext import RawClient, pool

_LOG = logging.getLogger(__name__)
_LOG_STR = "<<<!  #####  %s  #####  !>>>"

_IMPORTED: List[ModuleType] = []
_INIT_TASKS: List[asyncio.Task] = []
_START_TIME = time.time()


def _shutdown() -> None:
    _LOG.info(_LOG_STR, 'durdurma  talebi, görevler iptal ediliyor...')
    for task in asyncio.all_tasks():
        task.cancel()
    _LOG.info(_LOG_STR, 'tüm görevler iptal edildi !')


async def _complete_init_tasks() -> None:
    if not _INIT_TASKS:
        return
    await asyncio.gather(*_INIT_TASKS)
    _INIT_TASKS.clear()


class _AbstractUserge(Methods, RawClient):
    @property
    def is_bot(self) -> bool:
        """ döndüren değer bot mu değil mi"""
        if self._bot is not None:
            return hasattr(self, 'ubot')
        return bool(Config.BOT_TOKEN)

    @property
    def uptime(self) -> str:
        """ returns userge uptime """
        return time_formatter(time.time() - _START_TIME)

    async def finalize_load(self) -> None:
        """ finalize the plugins load """
        await asyncio.gather(_complete_init_tasks(), self.manager.init())

    async def load_plugin(self, name: str, reload_plugin: bool = False) -> None:
        """ Load plugin to Userge """
        _LOG.debug(_LOG_STR, f"{name} İçe aktarılıyor")
        _IMPORTED.append(
            importlib.import_module(f"userge.plugins.{name}"))
        if reload_plugin:
            _IMPORTED[-1] = importlib.reload(_IMPORTED[-1])
        plg = _IMPORTED[-1]
        self.manager.update_plugin(plg.__name__, plg.__doc__)
        if hasattr(plg, '_init'):
            # pylint: disable=protected-access
            if asyncio.iscoroutinefunction(plg._init):
                _INIT_TASKS.append(
                    asyncio.get_event_loop().create_task(plg._init()))
        _LOG.debug(_LOG_STR, f"{_IMPORTED[-1].__name__} Eklentisi Başarıyla İçe Aktarıldı")

    async def _load_plugins(self) -> None:
        _IMPORTED.clear()
        _INIT_TASKS.clear()
        logbot.edit_last_msg("Tüm Eklentiler İçe Aktarıldı", _LOG.info, _LOG_STR)
        for name in get_all_plugins():
            try:
                await self.load_plugin(name)
            except ImportError as i_e:
                _LOG.error(_LOG_STR, f"[{name}] - {i_e}")
        await self.finalize_load()
        _LOG.info(_LOG_STR, f"({len(_IMPORTED)})  => Eklentisi içe aktarıldı "
                  + str([i.__name__ for i in _IMPORTED]))

    async def reload_plugins(self) -> int:
        """ Reload all Plugins """
        self.manager.clear_plugins()
        reloaded: List[str] = []
        _LOG.info(_LOG_STR, "Tüm Eklentileri Yeniden Yüklendi")
        for imported in _IMPORTED:
            try:
                reloaded_ = importlib.reload(imported)
            except ImportError as i_e:
                _LOG.error(_LOG_STR, i_e)
            else:
                reloaded.append(reloaded_.__name__)
        _LOG.info(_LOG_STR, f" {len(reloaded)} Eklentisi  => {reloaded} Yeniden yüklendi")
        await self.finalize_load()
        return len(reloaded)


class _UsergeBot(_AbstractUserge):
    """ UsergeBot, the bot """
    def __init__(self, **kwargs) -> None:
        _LOG.info(_LOG_STR, "UsergeBot Yapılandırması Ayarlanıyor")
        super().__init__(session_name=":memory:", **kwargs)

    @property
    def ubot(self) -> 'Userge':
        """ returns userbot """
        return self._bot


class Userge(_AbstractUserge):
    """ Userge, the userbot """

    has_bot = bool(Config.BOT_TOKEN)

    def __init__(self, **kwargs) -> None:
        _LOG.info(_LOG_STR, "Userge Yapılandırması Ayarlanıyor")
        kwargs = {
            'api_id': Config.API_ID,
            'api_hash': Config.API_HASH,
            'workers': Config.WORKERS
        }
        if Config.BOT_TOKEN:
            kwargs['bot_token'] = Config.BOT_TOKEN
        if Config.HU_STRING_SESSION and Config.BOT_TOKEN:
            RawClient.DUAL_MODE = True
            kwargs['bot'] = _UsergeBot(bot=self, **kwargs)
        kwargs['session_name'] = Config.HU_STRING_SESSION or ":memory:"
        super().__init__(**kwargs)

    @property
    def bot(self) -> Union['_UsergeBot', 'Userge']:
        """ returns usergebot """
        if self._bot is None:
            if Config.BOT_TOKEN:
                return self
            raise UsergeBotNotFound("BOT_TOKEN ENV gerekiyor!")
        return self._bot

    async def start(self) -> None:
        """ start client and bot """
        pool._start()  # pylint: disable=protected-access
        _LOG.info(_LOG_STR, "USERGE-X Başlatılıyor")
        await super().start()
        if self._bot is not None:
            _LOG.info(_LOG_STR, "USERGE-X Bot Başlatılıyor")
            await self._bot.start()
        await self._load_plugins()

    async def stop(self) -> None:  # pylint: disable=arguments-differ
        """ stop client and bot """
        if self._bot is not None:
            _LOG.info(_LOG_STR, "USERGE-X Botunun Durduruluyor")
            await self._bot.stop()
        _LOG.info(_LOG_STR, "USERGE-X durduruluyor")
        await super().stop()
        await pool._stop()  # pylint: disable=protected-access

    def begin(self, coro: Optional[Awaitable[Any]] = None) -> None:
        """ start userge """
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGHUP, _shutdown)
        loop.add_signal_handler(signal.SIGTERM, _shutdown)
        run = loop.run_until_complete
        try:
            run(self.start())
            running_tasks: List[asyncio.Task] = []
            for task in self._tasks:
                running_tasks.append(loop.create_task(task()))
            if coro:
                _LOG.info(_LOG_STR, "Running Coroutine")
                run(coro)
            else:
                _LOG.info(_LOG_STR, "USERGE-X boşta çalıştırılıyor")
                logbot.edit_last_msg("USERGE-X  Başlatıldı!")
                logbot.end()
                idle()
            _LOG.info(_LOG_STR, "USERGE-X'ten çıkılıyor")
            for task in running_tasks:
                task.cancel()
            run(self.stop())
            run(loop.shutdown_asyncgens())
        except asyncio.exceptions.CancelledError:
            pass
        finally:
            if not loop.is_running():
                loop.close()
