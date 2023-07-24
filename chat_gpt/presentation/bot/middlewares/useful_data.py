from typing import Callable, Dict, Any, Awaitable, Optional
from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import TelegramObject
from chat_gpt.core.dto import UserGetByFilters
from chat_gpt.core.entities import User
from chat_gpt.core.use_cases import (
    UserGetOneByFiltersUseCase,
)


class UsefulDataMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        ioc = data["ioc"]
        user_get_one_by_filters_use_case: UserGetOneByFiltersUseCase = (
            await ioc.provider(UserGetOneByFiltersUseCase)
        )

        useful_data: dict[str, Optional[User]] = {
            "user": None,
        }

        user_tg = data["event_from_user"]
        if user_tg is not None:
            user_tg_id = user_tg.id
            user = await user_get_one_by_filters_use_case.execute(
                UserGetByFilters(
                    id=user_tg_id,
                )
            )
            if user is not None:
                useful_data["user"] = user

        data["useful_data"] = useful_data
        return await handler(event, data)


def register_middleware(dp: Dispatcher):
    useful_data_user_middleware = UsefulDataMiddleware()
    dp.update.middleware(useful_data_user_middleware)
