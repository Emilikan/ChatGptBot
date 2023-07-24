from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Text
from chat_gpt.presentation.di import IoC
from chat_gpt.presentation.bot.keyboards.default import (
    btn_reset_limit_requests,
)
from chat_gpt.presentation.bot.states import AdminMenu
from chat_gpt.core.dto import UserResetLimitRequests
from chat_gpt.core.use_cases import UserResetLimitRequestsUseCase

router = Router()


@router.message(AdminMenu.menu, Text(btn_reset_limit_requests))
async def add_admin(
    message: Message,
    ioc: IoC,
):
    user_reset_limit_requests_use_case: UserResetLimitRequestsUseCase = (
        await ioc.provider(UserResetLimitRequestsUseCase)
    )
    await user_reset_limit_requests_use_case.execute(UserResetLimitRequests())
