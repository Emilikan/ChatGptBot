from typing import Dict
from aiogram import Bot, Router, F
from aiogram.types import Message, ContentType
from aiogram.fsm.context import FSMContext
from chat_gpt.presentation.di import IoC
from chat_gpt.presentation.bot.filters import ChatTypeFilter, UserAccess
from chat_gpt.core.dto import SendQuery
from chat_gpt.core.use_cases import SendQueryUseCase


router = Router()


@router.message(
    ChatTypeFilter(["private"]),
    UserAccess(),
    F.content_type.in_([ContentType.TEXT]),
)
async def text_query(
    message: Message,
    useful_data: Dict,
    state: FSMContext,
    bot: Bot,
    ioc: IoC,
):
    send_query_use_case: SendQueryUseCase = await ioc.provider(
        SendQueryUseCase
    )
    user = useful_data["user"]
    text = message.text
    answer = await send_query_use_case.execute(
        SendQuery(
            user_id=user.id,
            query_text=text,  # type: ignore
        )
    )
    await message.answer(answer)
