from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from chat_gpt.presentation.bot.keyboards.default.shared import (
    btn_exit,
)

btn_show_users = "Пользователи"
btn_show_admin = "👨‍💻 Администраторы"
btn_reset_limit_requests = "Сбросить лимиты запросов"


def start(is_main_admin=False):
    builder = ReplyKeyboardBuilder()
    btn_texts = [
        btn_show_users,
    ]
    if is_main_admin:
        btn_texts.append(btn_show_admin)
    btn_texts.append(btn_reset_limit_requests)
    btn_texts.append(btn_exit)
    for btn_text in btn_texts:
        builder.add(KeyboardButton(text=btn_text))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
