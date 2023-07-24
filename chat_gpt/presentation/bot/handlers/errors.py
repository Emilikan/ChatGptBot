from typing import Any
import logging
from aiogram import Router, Bot
from aiogram.types import ErrorEvent
from aiogram_dialog import DialogManager

router = Router()


@router.errors()
async def error_handler(
    err: ErrorEvent, bot: Bot, dialog_manager: DialogManager
) -> Any:
    logging.error(err.exception)
    chat_id = err.update.message.chat.id
    if err.update.callback_query:
        chat_id = err.update.callback_query.message.chat.id
    await bot.send_message(chat_id, "Произошла ошибка, нажмите /start")
    await dialog_manager.reset_stack()


def get_errors_router() -> Router:
    return router
