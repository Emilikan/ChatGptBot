from di import ScopeState
from chat_gpt.config import Settings
from chat_gpt.presentation.di import DIContainer, DIScope, IoC
from chat_gpt.core.dto import UserGetByFilters, AdminCreate
from chat_gpt.core.use_cases import (
    UserGetByFiltersUseCase,
    AdminCreateUseCase,
)


async def initial_initialization(
    settings: Settings,
    di_container: DIContainer,
    app_state: ScopeState,
    ioc: IoC,
):
    async with di_container.enter_scope(
        DIScope.REQUEST, app_state
    ) as request_state:
        ioc.set_scope_and_state(request_state, DIScope.REQUEST)
        admin_create_use_case: AdminCreateUseCase = await ioc.provider(
            AdminCreateUseCase
        )
        user_get_by_filters_use_case: UserGetByFiltersUseCase = (
            await ioc.provider(UserGetByFiltersUseCase)
        )

        for admin_id in settings.admins:
            users = await user_get_by_filters_use_case.execute(
                UserGetByFilters(
                    telegram_id=admin_id,
                )
            )
            if not users:
                return
            user = users[0]
            if user:
                try:
                    await admin_create_use_case.execute(
                        AdminCreate(user_id=user.id)
                    )
                except Exception:
                    ...
