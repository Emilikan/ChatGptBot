from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Row
from aiogram_dialog.widgets.text import Const, Format
from chat_gpt.core.dto import UserRemoveAccess, UserContextCleare
from chat_gpt.core.use_cases import (
    UserRemoveAccessUseCase,
    UserContextCleareUseCase,
)
from ..states import ShowUsers


async def user_info_start(
    c: CallbackQuery, button: Button, manager: DialogManager
):
    await manager.switch_to(ShowUsers.user_info)


async def get_window_data(dialog_manager: DialogManager, **kwargs):
    user = dialog_manager.dialog_data["current_user"]
    data = {
        "telegram": user["name"],
    }
    return data


async def delete(c: CallbackQuery, button: Button, manager: DialogManager):
    ioc = manager.middleware_data["ioc"]
    user = manager.dialog_data["current_user"]

    user_remove_access_use_case: UserRemoveAccessUseCase = await ioc.provider(
        UserRemoveAccessUseCase
    )
    await user_remove_access_use_case.execute(
        UserRemoveAccess(user_id=user["id"])
    )
    manager.show_mode = ShowMode.SEND
    await manager.switch_to(ShowUsers.main)


async def cleare_context(
    c: CallbackQuery, button: Button, manager: DialogManager
):
    ioc = manager.middleware_data["ioc"]
    user = manager.dialog_data["current_user"]

    user_context_cleare_use_case: UserContextCleareUseCase = (
        await ioc.provider(UserContextCleareUseCase)
    )
    await user_context_cleare_use_case.execute(
        UserContextCleare(user_id=user["id"])
    )
    manager.show_mode = ShowMode.SEND
    await manager.switch_to(ShowUsers.main)


user_info_window = Window(
    Format("Пользователь: @{telegram}"),
    Row(
        Button(
            Const("Удалить"),
            id="delete",
            on_click=delete,
        ),
    ),
    Row(
        Button(
            Const("Очистить контекст"),
            id="cleare_context",
            on_click=cleare_context,
        ),
    ),
    SwitchTo(
        Const("Назад"),
        id="exit",
        state=ShowUsers.main,
    ),
    getter=get_window_data,
    state=ShowUsers.user_info,
)
