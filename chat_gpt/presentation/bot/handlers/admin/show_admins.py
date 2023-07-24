from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Text
from aiogram_dialog import DialogManager, StartMode
from chat_gpt.presentation.bot.filters import IsMainAdmin
from chat_gpt.presentation.bot.keyboards.default import (
    btn_show_admin,
)
from chat_gpt.presentation.bot.dialogs import ShowAdmins
from chat_gpt.presentation.bot.states import AdminMenu

router = Router()


@router.message(AdminMenu.menu, IsMainAdmin(), Text(btn_show_admin))
async def add_admin(
    message: Message, dialog_manager: DialogManager, *args, **kwargs
):
    await dialog_manager.start(
        ShowAdmins.main,
        mode=StartMode.RESET_STACK,
    )
