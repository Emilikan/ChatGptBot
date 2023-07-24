from typing import Dict
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Cancel, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Multi, Format, Const
from chat_gpt.core.dto import UserGetByFilters
from chat_gpt.core.use_cases import (
    UserGetByFiltersUseCase,
)
from .states import ShowAdmins
from .windows import (
    admin_info_window,
    add_admin_window,
    add_admin_start,
)


async def get_start_data(start_data: Dict, manager: DialogManager):
    manager.dialog_data.update(
        {
            "admins_data": [],
        }
    )
    if start_data:
        manager.dialog_data.update(start_data)


async def loaded_data(manager: DialogManager):
    ioc = manager.middleware_data["ioc"]

    user_get_by_filters_use_case: UserGetByFiltersUseCase = await ioc.provider(
        UserGetByFiltersUseCase
    )  # noqa

    admins = await user_get_by_filters_use_case.execute(
        UserGetByFilters(is_admin=True)
    )
    admins_data = {}
    for admin in admins:
        admins_data[admin.name] = {
            "id": admin.id,
            "name": admin.name,
            "is_admin": admin.is_admin,
        }

    manager.dialog_data.update(
        {
            "admins_data": admins_data,
        }
    )


async def get_window_main_data(dialog_manager: DialogManager, **kwargs):
    dialog_data = dialog_manager.dialog_data
    await loaded_data(dialog_manager)
    data = {"admins_data": dialog_data["admins_data"]}
    return data


async def admins_selected(
    c: CallbackQuery,
    select: Select,
    manager: DialogManager,
    admin_tg_name: str,
):
    admin = manager.dialog_data["admins_data"][admin_tg_name]
    manager.dialog_data["current_admin"] = {
        **admin,
    }
    await manager.switch_to(ShowAdmins.admin_info)


admin_list = ScrollingGroup(
    Select(
        Format("@{item}"),
        id="s_admins",
        item_id_getter=lambda x: x,
        items="admins_data",
        on_click=admins_selected,
    ),
    id="scroll_admin_list",
    height=3,
    width=1,
)
btn_add_admin = Button(
    Const("Добавить"),
    id="add_admin",
    on_click=add_admin_start,
)

main_window = Window(
    Multi(
        Const("Админы"),
    ),
    admin_list,
    btn_add_admin,
    Cancel(Const("отмена")),
    getter=get_window_main_data,
    state=ShowAdmins.main,
)

ui = Dialog(
    main_window,
    admin_info_window,
    add_admin_window,
    on_start=get_start_data,
)
