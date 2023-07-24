from aiogram import Bot, Router
from aiogram.filters import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from chat_gpt.config import Settings
from chat_gpt.presentation.di import IoC
from chat_gpt.presentation.bot.keyboards.default import btn_admin
from chat_gpt.presentation.bot.filters import IsAdmin, ChatTypeFilter
from chat_gpt.presentation.bot.states import AdminMenu
from chat_gpt.core.protocols import AdminView


router = Router()


@router.message(ChatTypeFilter(["private"]), Text(btn_admin), IsAdmin())
async def admin_start(
    message: Message, state: FSMContext, bot: Bot, ioc: IoC, settings: Settings
):
    admin_view: AdminView = await ioc.provider(AdminView)

    user_tg_id = message.from_user.id
    is_main_admin = user_tg_id == settings.main_admin

    await admin_view.greeting(user_tg_id, is_main_admin)

    await state.set_state(AdminMenu.menu)
