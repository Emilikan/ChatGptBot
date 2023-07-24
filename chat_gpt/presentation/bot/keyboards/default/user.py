from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

btn_admin = "👨‍💻 Админ"


def start(is_admin=False):
    builder = ReplyKeyboardBuilder()
    btn_texts = []
    if is_admin:
        btn_texts.append(btn_admin)
    for btn_text in btn_texts:
        builder.add(types.KeyboardButton(text=btn_text))
    builder.adjust(2)
    if len(builder.as_markup().keyboard) == 0:
        return types.ReplyKeyboardRemove()
    return builder.as_markup(resize_keyboard=True)
