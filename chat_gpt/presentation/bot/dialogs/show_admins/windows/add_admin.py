from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.input import MessageInput
from chat_gpt.core.protocols import AdminView
from chat_gpt.core.dto import UserGetByFilters, AdminCreate
from chat_gpt.core.use_cases import (
    UserGetByFiltersUseCase,
    AdminCreateUseCase,
)
from ..states import ShowAdmins


async def add_admin_start(
    c: CallbackQuery, button: Button, manager: DialogManager
):
    await manager.switch_to(ShowAdmins.add_admin)


async def add_admin(m: Message, dialog: Dialog, manager: DialogManager):
    ioc = manager.middleware_data["ioc"]

    admin_view: AdminView = await ioc.provider(AdminView)
    user_get_by_filters: UserGetByFiltersUseCase = await ioc.provider(
        UserGetByFiltersUseCase
    )
    admin_create_use_case: AdminCreateUseCase = await ioc.provider(
        AdminCreateUseCase
    )

    user_tg_id = m.from_user.id
    admin_tg_name = m.text.replace("@", "")

    users = await user_get_by_filters.execute(
        UserGetByFilters(
            name=admin_tg_name,
        )
    )
    if not users:
        await admin_view.user_not_found(user_tg_id)
        await manager.switch_to(ShowAdmins.main)
        return
    user = users[0]

    await admin_create_use_case.execute(AdminCreate(user_id=user.id))
    await admin_view.inform_that_user_become_admin(user.id)
    await m.answer("Админ добавлен")
    await manager.switch_to(ShowAdmins.main)


add_admin_window = Window(
    Format("Введите имя пользователя без @"),
    MessageInput(add_admin),
    state=ShowAdmins.add_admin,
)
