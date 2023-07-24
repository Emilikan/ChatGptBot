from typing import Dict
from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from chat_gpt.presentation.di import IoC
from chat_gpt.presentation.bot.keyboards.default import btn_exit
from chat_gpt.presentation.bot.states import AdminMenu
from chat_gpt.core.protocols import UserView
from chat_gpt.core.dto import UserShowMenu


router = Router()


@router.message(AdminMenu.menu, Text(btn_exit))
async def admin_exit(
    message: Message,
    useful_data: Dict,
    state: FSMContext,
    ioc: IoC,
):
    user_view: UserView = await ioc.provider(UserView)

    user_tg_id = message.from_user.id

    user = useful_data["user"]
    await user_view.show_menu(
        UserShowMenu(
            chat_id=user_tg_id,
            is_admin=user.is_admin,
        )
    )
    await state.clear()
