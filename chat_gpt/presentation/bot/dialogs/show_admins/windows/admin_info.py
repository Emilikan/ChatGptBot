from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Row
from aiogram_dialog.widgets.text import Const, Format
from chat_gpt.core.protocols import AdminView
from chat_gpt.core.dto import AdminDelete
from chat_gpt.core.use_cases import AdminDeleteUseCase
from ..states import ShowAdmins


async def admin_info_start(
    c: CallbackQuery, button: Button, manager: DialogManager
):
    await manager.switch_to(ShowAdmins.admin_info)


async def get_window_data(dialog_manager: DialogManager, **kwargs):
    admin = dialog_manager.dialog_data["current_admin"]
    data = {
        "telegram": admin["name"],
    }
    return data


async def delete(c: CallbackQuery, button: Button, manager: DialogManager):
    ioc = manager.middleware_data["ioc"]
    bot: Bot = manager.middleware_data["bot"]
    dp: Dispatcher = manager.middleware_data["dp"]
    admin = manager.dialog_data["current_admin"]

    admin_view: AdminView = await ioc.provider(AdminView)
    admin_delete_use_case: AdminDeleteUseCase = await ioc.provider(
        AdminDeleteUseCase
    )
    user_state: FSMContext = dp.fsm.resolve_context(
        bot, chat_id=admin["id"], user_id=admin["id"]
    )
    admin_dialog_manager = manager.bg(user_id=admin["id"], chat_id=admin["id"])
    await admin_dialog_manager.done()
    await admin_delete_use_case.execute(AdminDelete(user_id=admin["id"]))
    await user_state.clear()

    manager.show_mode = ShowMode.SEND
    await admin_view.inform_that_user_stopped_being_admin(chat_id=admin["id"])
    await manager.switch_to(ShowAdmins.main)


admin_info_window = Window(
    Format("Админ: @{telegram}"),
    Row(
        Button(
            Const("Удалить"),
            id="delete",
            on_click=delete,
        ),
    ),
    SwitchTo(
        Const("Назад"),
        id="exit",
        state=ShowAdmins.main,
    ),
    getter=get_window_data,
    state=ShowAdmins.admin_info,
)
