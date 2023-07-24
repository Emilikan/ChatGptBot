from aiogram import Dispatcher

from di import ScopeState
from chat_gpt.config import Settings
from chat_gpt.presentation.di import DIContainer, IoC


def register_middlewares(
    dp: Dispatcher,
    settings: Settings,
    container: DIContainer,
    app_state: ScopeState,
    ioc: IoC,
):
    from . import throttling, di, useful_data

    throttling.register_middleware(dp=dp, settings=settings)
    di.register_middleware(
        dp=dp, container=container, app_state=app_state, ioc=ioc
    )
    useful_data.register_middleware(dp)
