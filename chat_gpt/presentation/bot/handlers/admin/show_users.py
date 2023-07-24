from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Text
from aiogram_dialog import DialogManager, StartMode
from chat_gpt.presentation.bot.keyboards.default import (
    btn_admin_show_users,
)
from chat_gpt.presentation.bot.dialogs import ShowUsers
from chat_gpt.presentation.bot.states import AdminMenu

router = Router()


@router.message(AdminMenu.menu, Text(btn_admin_show_users))
async def add_admin(
    message: Message, dialog_manager: DialogManager, *args, **kwargs
):
    await dialog_manager.start(
        ShowUsers.main,
        mode=StartMode.RESET_STACK,
    )
