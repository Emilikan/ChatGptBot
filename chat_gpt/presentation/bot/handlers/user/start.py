from typing import Dict
from aiogram import Bot, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from chat_gpt.presentation.di import IoC
from chat_gpt.presentation.bot.filters import ChatTypeFilter
from chat_gpt.core.protocols import UserView
from chat_gpt.core.dto import UserCreate, UserShowMenu
from chat_gpt.core.use_cases import UserCreateUseCase


router = Router()


@router.message(ChatTypeFilter(["private"]), CommandStart())
async def user_start(
    message: Message,
    useful_data: Dict,
    state: FSMContext,
    bot: Bot,
    ioc: IoC,
):
    user_create_handler: UserCreateUseCase = await ioc.provider(
        UserCreateUseCase
    )

    user_view: UserView = await ioc.provider(UserView)

    user = useful_data["user"]
    user_tg_id = message.from_user.id
    username = message.from_user.username
    if username is None:
        await message.answer(
            'Заполните поле "Имя пользователя" в настройках'
            + ", а потом нажмите /start"
        )
        return

    if not user:
        user = await user_create_handler.execute(
            UserCreate(id=user_tg_id, name=username)
        )

    await state.clear()
    await user_view.greeting(
        UserShowMenu(
            chat_id=user_tg_id,
            is_admin=user.is_admin,
        )
    )
