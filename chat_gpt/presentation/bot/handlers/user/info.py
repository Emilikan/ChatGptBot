from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message

from chat_gpt.presentation.bot.commands import (
    owner_commands,
    users_commands,
)
from chat_gpt.config import Settings
from chat_gpt.presentation.bot.keyboards.inline import get_author_keyboard

router = Router()


@router.message(Command(commands=["help"]))
async def help_handler(message: Message, settings: Settings):
    text = "ℹ️ <b>Список команд:</b> \n\n"
    commands = (
        owner_commands.items()
        if message.from_user.id == settings.bot_.owner_id
        else users_commands.items()
    )
    for command, description in commands:
        text += f"/{command} - <b>{description}</b> \n"
    await message.answer(text)


@router.message(Command(commands=["about"]))
async def about_handler(message: Message, bot: Bot, settings: Settings):
    bot_information = await bot.get_me()
    await message.answer(
        "<b>ℹ️ Информация о боте:</b> \n\n"
        f"<b>Название - </b> {bot_information.full_name} \n"
        f"<b>Username - </b> @{bot_information.username} \n"
        f"<b>ID - </b> <code>{bot_information.id}</code> \n",
        reply_markup=get_author_keyboard(owner_id=settings.bot_.owner_id),
    )
