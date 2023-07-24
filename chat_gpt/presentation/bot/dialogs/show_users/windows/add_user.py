from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.input import MessageInput
from chat_gpt.core.protocols import UserView
from chat_gpt.core.dto import UserGetByFilters, UserGiveAccess
from chat_gpt.core.use_cases import (
    UserGetByFiltersUseCase,
    UserGiveAccessUseCase,
)
from ..states import ShowUsers


async def add_user_start(
    c: CallbackQuery, button: Button, manager: DialogManager
):
    await manager.switch_to(ShowUsers.add_user)


async def add_user(m: Message, dialog: Dialog, manager: DialogManager):
    ioc = manager.middleware_data["ioc"]

    user_view: UserView = await ioc.provider(UserView)
    user_get_by_filters: UserGetByFiltersUseCase = await ioc.provider(
        UserGetByFiltersUseCase
    )
    user_give_access_use_case: UserGiveAccessUseCase = await ioc.provider(
        UserGiveAccessUseCase
    )

    user_tg_id = m.from_user.id
    user_tg_name = m.text

    users = await user_get_by_filters.execute(
        UserGetByFilters(
            name=user_tg_name,
        )
    )
    if not users:
        await user_view.user_not_found(user_tg_id)
        await manager.switch_to(ShowUsers.main)
        return
    user = users[0]

    await user_give_access_use_case.execute(UserGiveAccess(user_id=user.id))
    await user_view.inform_that_user_give_access(user.id)
    await m.answer("Пользователь добавлен")
    await manager.switch_to(ShowUsers.main)


add_user_window = Window(
    Format("Введите имя пользователя без @"),
    MessageInput(add_user),
    state=ShowUsers.add_user,
)
