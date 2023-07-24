import asyncio
import logging

import coloredlogs
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)
from aiogram_dialog import setup_dialogs
from aiohttp import web

from chat_gpt.config import Settings
from chat_gpt.infrastructure.storage.sqlalchemy import db_mappers
from chat_gpt.presentation.bot.handlers import get_handlers_router
from chat_gpt.presentation.bot.dialogs import register_dialogs
from chat_gpt.presentation.bot.middlewares import register_middlewares
from chat_gpt.presentation.bot.commands import (
    remove_bot_commands,
    setup_bot_commands,
)
from di import ScopeState
from chat_gpt.presentation.di import DIContainer, DIScope, IoC, IoCImpl
from chat_gpt.presentation.bot.di.builds import build_container
from chat_gpt.config import initial_initialization


async def on_startup(
    dispatcher: Dispatcher,
    bot: Bot,
    settings: Settings,
    container: DIContainer,
    app_state: ScopeState,
    ioc: IoC,
):
    register_middlewares(
        dp=dispatcher,
        settings=settings,
        container=container,
        app_state=app_state,
        ioc=ioc,
    )

    register_dialogs(dispatcher)
    dispatcher.include_router(get_handlers_router())
    setup_dialogs(dispatcher)

    await setup_bot_commands(bot, settings)
    if settings.webhook.use:
        webhook_url = (
            settings.webhook.url + settings.webhook.path
            if settings.webhook.url
            else "http://localhost:{port}{path}".format(
                port=settings.webhook.port, path=settings.webhook.path
            )
        )
        await bot.set_webhook(
            webhook_url,
            drop_pending_updates=settings.webhook.drop_pending_updates,
            allowed_updates=dispatcher.resolve_used_update_types(),
        )
    else:
        await bot.delete_webhook(
            drop_pending_updates=settings.webhook.drop_pending_updates,
        )

    db_mappers()
    await initial_initialization(
        settings=settings, di_container=container, app_state=app_state, ioc=ioc
    )
    bot_info = await bot.get_me()

    logging.info(f"Name - {bot_info.full_name}")
    logging.info(f"Username - @{bot_info.username}")
    logging.info(f"ID - {bot_info.id}")

    states = {
        True: "Enabled",
        False: "Disabled",
    }

    logging.debug(f"Groups Mode - {states[bot_info.can_join_groups]}")  # type: ignore # noqa
    logging.debug(
        f"Privacy Mode - {states[not bot_info.can_read_all_group_messages]}"
    )
    logging.debug(f"Inline Mode - {states[bot_info.supports_inline_queries]}")  # type: ignore # noqa

    logging.info("Bot started!")


async def on_shutdown(dispatcher: Dispatcher, bot: Bot, settings: Settings):
    logging.warning("Stopping bot...")
    await remove_bot_commands(bot, settings)
    await bot.delete_webhook(
        drop_pending_updates=settings.webhook.drop_pending_updates
    )
    await dispatcher.fsm.storage.close()
    await bot.session.close()


async def main():
    coloredlogs.install(level=logging.INFO)
    logging.warning("Starting bot...")

    settings = Settings()

    session = AiohttpSession(
        api=TelegramAPIServer.from_base(
            settings.bot_.api_url, is_local=settings.bot_.api_is_local
        )
    )
    token = settings.bot_.token

    bot_settings = {
        "session": session,
        "parse_mode": "HTML",
    }

    bot = Bot(token, **bot_settings)

    if settings.bot_.redis_use:
        storage = RedisStorage.from_url(
            settings.redis_.url,
            key_builder=DefaultKeyBuilder(with_destiny=True),
        )
    else:
        storage = MemoryStorage()

    dp = Dispatcher(storage=storage)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    container = build_container(settings, bot)
    ioc = IoCImpl(di_container=container)

    async with container.enter_scope(DIScope.APP) as app_state:
        context_kwargs = {
            "dp": dp,
            "settings": settings,
            "container": container,
            "app_state": app_state,
            "ioc": ioc,
        }
    if settings.webhook.use:
        logging.getLogger("aiohttp.access").setLevel(logging.CRITICAL)

        web_app = web.Application()
        SimpleRequestHandler(
            dispatcher=dp, bot=bot, **context_kwargs
        ).register(web_app, path=settings.webhook.path)

        setup_application(web_app, dp, bot=bot, **context_kwargs)

        runner = web.AppRunner(web_app)
        await runner.setup()
        site = web.TCPSite(runner, port=settings.webhook.port)
        await site.start()

        await asyncio.Event().wait()
    else:
        await dp.start_polling(bot, **context_kwargs)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
