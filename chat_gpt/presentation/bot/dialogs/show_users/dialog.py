from typing import Dict
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Cancel, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format, Const
from chat_gpt.core.dto import UserGetByFilters, UserContextCleareAll
from chat_gpt.core.use_cases import (
    UserGetByFiltersUseCase,
    UserContextCleareAllUseCase,
)
from .states import ShowUsers
from .windows import (
    user_info_window,
    add_user_window,
    add_user_start,
)


async def get_start_data(start_data: Dict, manager: DialogManager):
    manager.dialog_data.update(
        {
            "users_data": [],
        }
    )
    if start_data:
        manager.dialog_data.update(start_data)


async def loaded_data(manager: DialogManager):
    ioc = manager.middleware_data["ioc"]

    user_get_by_filters_use_case: UserGetByFiltersUseCase = await ioc.provider(
        UserGetByFiltersUseCase
    )  # noqa

    users = await user_get_by_filters_use_case.execute(
        UserGetByFilters(access=True)
    )
    users_data = {}
    for user in users:
        users_data[user.name] = {
            "id": user.id,
            "name": user.name,
            "access": user.access,
            "is_admin": user.is_admin,
        }

    manager.dialog_data.update(
        {
            "users_data": users_data,
        }
    )


async def get_window_main_data(dialog_manager: DialogManager, **kwargs):
    dialog_data = dialog_manager.dialog_data
    await loaded_data(dialog_manager)
    data = {"users_data": dialog_data["users_data"]}
    return data


async def users_selected(
    c: CallbackQuery,
    select: Select,
    manager: DialogManager,
    user_tg_name: str,
):
    user = manager.dialog_data["users_data"][user_tg_name]
    manager.dialog_data["current_user"] = {
        **user,
    }
    await manager.switch_to(ShowUsers.user_info)


async def cleare_all_context(
    c: CallbackQuery, button: Button, manager: DialogManager
):
    ioc = manager.middleware_data["ioc"]

    user_context_cleare_all_use_case: UserContextCleareAllUseCase = (
        await ioc.provider(UserContextCleareAllUseCase)
    )
    await user_context_cleare_all_use_case.execute(UserContextCleareAll())

    await manager.switch_to(ShowUsers.main)


user_list = ScrollingGroup(
    Select(
        Format("@{item}"),
        id="s_users",
        item_id_getter=lambda x: x,
        items="users_data",
        on_click=users_selected,
    ),
    id="scroll_user_list",
    height=3,
    width=1,
)
btn_add_user = Button(
    Const("Добавить"),
    id="add_user",
    on_click=add_user_start,
)
btn_cleare_all_context = Button(
    Const("Очистить контекст всех пользователей"),
    id="cleare_all_context",
    on_click=cleare_all_context,
)

main_window = Window(
    Const("Пользователи"),
    user_list,
    btn_add_user,
    btn_cleare_all_context,
    Cancel(Const("отмена")),
    getter=get_window_main_data,
    state=ShowUsers.main,
)

ui = Dialog(
    main_window,
    user_info_window,
    add_user_window,
    on_start=get_start_data,
)
