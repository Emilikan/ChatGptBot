from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import TelegramObject
from cachetools import TTLCache

from chat_gpt.config import Settings


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, settings: Settings):
        self.cache = TTLCache(
            maxsize=10_000, ttl=settings.bot_.throttling_rate
        )
        self.cache_for_answer = TTLCache(maxsize=10_000, ttl=5)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        chat_id = data["event_chat"].id
        if chat_id in self.cache:
            bot = data["bot"]
            if chat_id not in self.cache_for_answer:
                await bot.send_message(
                    chat_id=chat_id, text="Слишком частные запросы"
                )
                self.cache_for_answer[chat_id] = None
            self.cache[chat_id] = None
            return
        self.cache[chat_id] = None
        return await handler(event, data)


def register_middleware(dp: Dispatcher, settings: Settings):
    throttling_middleware = ThrottlingMiddleware(settings=settings)
    dp.update.middleware(throttling_middleware)
