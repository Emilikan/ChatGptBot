from typing import Optional, Any
import inspect
from aiogram import Bot
from di.api.dependencies import DependentBase
from di.dependent import Dependent
from di import Container, bind_by_type
from sqlalchemy.ext.asyncio import AsyncSession
from chat_gpt.presentation.di import DIContainer, DIScope

from chat_gpt.config import Settings
from chat_gpt.core.protocols import ChatGpt
from chat_gpt.infrastructure.chat_gpt import ChatGptImpl

from chat_gpt.infrastructure.storage.sqlalchemy import (
    create_session_factory,
)
from chat_gpt.core.protocols import (
    Commiter,
    UserGateway,
    UserContextGateway,
)
from chat_gpt.infrastructure.storage.sqlalchemy.gateway import (
    CommiterImp,
    UserGatewayImpl,
    UserContextGatewayImpl,
)

from chat_gpt.core.protocols import (
    SharedView,
    UserView,
    AdminView,
)
from chat_gpt.presentation.bot.views import (
    SharedViewImpl,
    UserViewImpl,
    AdminViewImpl,
)


from chat_gpt.core.use_cases import (
    UserCreateUseCase,
    UserGetByFiltersUseCase,
    UserGetOneByFiltersUseCase,
    UserGiveAccessUseCase,
    UserRemoveAccessUseCase,
    UserResetLimitRequestsUseCase,
    AdminCreateUseCase,
    AdminDeleteUseCase,
    UserContextCreateUseCase,
    UserContextGetByFiltersUseCase,
    UserContextGetOneByFiltersUseCase,
    UserContextUpdateUseCase,
    UserContextDeleteUseCase,
    UserContextCleareUseCase,
    UserContextCleareAllUseCase,
)


def build_container(settigs: Settings, bot: Bot) -> DIContainer:
    container = Container()
    container.bind(match_request)
    container.bind(
        bind_by_type(
            Dependent(lambda: Settings(), scope=DIScope.APP), Settings  # type: ignore # noqa
        )
    )
    container.bind(
        bind_by_type(Dependent(lambda: bot, scope=DIScope.APP), Bot)
    )
    container.bind(
        bind_by_type(
            Dependent(create_session_factory, scope=DIScope.REQUEST),
            AsyncSession,
        )
    )
    build_gateways(container)
    build_views(container)
    build_another(container)
    build_use_cases(container)
    return DIContainer(container, (DIScope.APP, DIScope.REQUEST))


def build_gateways(container: Container) -> None:
    container.bind(
        bind_by_type(Dependent(CommiterImp, scope=DIScope.REQUEST), Commiter),
    )
    container.bind(
        bind_by_type(
            Dependent(UserGatewayImpl, scope=DIScope.REQUEST), UserGateway
        )
    )
    container.bind(
        bind_by_type(
            Dependent(UserContextGatewayImpl, scope=DIScope.REQUEST),
            UserContextGateway,
        )
    )


def build_views(container: Container) -> None:
    container.bind(
        bind_by_type(
            Dependent(SharedViewImpl, scope=DIScope.REQUEST), SharedView
        ),
    )

    container.bind(
        bind_by_type(Dependent(UserViewImpl, scope=DIScope.REQUEST), UserView),
    )
    container.bind(
        bind_by_type(
            Dependent(AdminViewImpl, scope=DIScope.REQUEST),
            AdminView,
        ),
    )


def build_use_cases(container: Container):
    container.bind(
        bind_by_type(
            Dependent(UserCreateUseCase, scope=DIScope.REQUEST),
            UserCreateUseCase,
        )
    )
    container.bind(
        bind_by_type(
            Dependent(UserGetByFiltersUseCase, scope=DIScope.REQUEST),
            UserGetByFiltersUseCase,
        )
    )
    container.bind(
        bind_by_type(
            Dependent(UserGetOneByFiltersUseCase, scope=DIScope.REQUEST),
            UserGetOneByFiltersUseCase,
        )
    )
    container.bind(
        bind_by_type(
            Dependent(UserGiveAccessUseCase, scope=DIScope.REQUEST),
            UserGiveAccessUseCase,
        )
    )
    container.bind(
        bind_by_type(
            Dependent(UserRemoveAccessUseCase, scope=DIScope.REQUEST),
            UserRemoveAccessUseCase,
        )
    )
    container.bind(
        bind_by_type(
            Dependent(UserResetLimitRequestsUseCase, scope=DIScope.REQUEST),
            UserResetLimitRequestsUseCase,
        )
    )
    container.bind(
        bind_by_type(
            Dependent(AdminCreateUseCase, scope=DIScope.REQUEST),
            AdminCreateUseCase,
        )
    )
    container.bind(
        bind_by_type(
            Dependent(AdminDeleteUseCase, scope=DIScope.REQUEST),
            AdminDeleteUseCase,
        )
    )
    container.bind(
        bind_by_type(
            Dependent(AdminDeleteUseCase, scope=DIScope.REQUEST),
            AdminDeleteUseCase,
        )
    )
    container.bind(
        bind_by_type(
            Dependent(UserContextCreateUseCase, scope=DIScope.REQUEST),
            UserContextCreateUseCase,
        )
    )
    container.bind(
        bind_by_type(
            Dependent(UserContextGetByFiltersUseCase, scope=DIScope.REQUEST),
            UserContextGetByFiltersUseCase,
        )
    )
    container.bind(
        bind_by_type(
            Dependent(
                UserContextGetOneByFiltersUseCase, scope=DIScope.REQUEST
            ),
            UserContextGetOneByFiltersUseCase,
        )
    )
    container.bind(
        bind_by_type(
            Dependent(UserContextUpdateUseCase, scope=DIScope.REQUEST),
            UserContextUpdateUseCase,
        )
    )
    container.bind(
        bind_by_type(
            Dependent(UserContextDeleteUseCase, scope=DIScope.REQUEST),
            UserContextDeleteUseCase,
        )
    )
    container.bind(
        bind_by_type(
            Dependent(UserContextCleareUseCase, scope=DIScope.REQUEST),
            UserContextCleareUseCase,
        )
    )
    container.bind(
        bind_by_type(
            Dependent(UserContextCleareAllUseCase, scope=DIScope.REQUEST),
            UserContextCleareAllUseCase,
        )
    )


def build_another(container: Container):
    container.bind(
        bind_by_type(Dependent(ChatGptImpl, scope=DIScope.REQUEST), ChatGpt)
    )


def match_request(
    param: Optional[inspect.Parameter],
    dependent: DependentBase[Any],
) -> Optional[DependentBase[Any]]:
    return None
