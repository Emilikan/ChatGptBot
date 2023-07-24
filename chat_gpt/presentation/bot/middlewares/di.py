from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import TelegramObject
from di import ScopeState
from chat_gpt.presentation.di import DIContainer, DIScope, IoC


class DIMiddleware(BaseMiddleware):
    def __init__(
        self, container: DIContainer, app_state: ScopeState, ioc: IoC
    ):
        self.container = container
        self.app_state = app_state
        self._ioc = ioc

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.container.enter_scope(
            DIScope.REQUEST, self.app_state
        ) as request_state:
            self._ioc.set_scope_and_state(request_state, DIScope.REQUEST)
            data["ioc"] = self._ioc
            return await handler(event, data)


def register_middleware(
    dp: Dispatcher, container: DIContainer, app_state: ScopeState, ioc: IoC
):
    di_middleware = DIMiddleware(container, app_state, ioc=ioc)
    dp.update.middleware(di_middleware)
