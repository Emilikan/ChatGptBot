from typing import Optional
from .base import BaseView
from chat_gpt.core.protocols import UserView
from chat_gpt.presentation.bot.keyboards.default.user import start
from chat_gpt.core.dto import UserShowMenu


class UserViewImpl(BaseView, UserView):
    async def greeting(self, data: UserShowMenu):
        bot_info = await self._bot.get_me()
        text = (
            f"Приветствую тебя в <b>{bot_info.full_name}</b>! \n"
            + "<b>ℹ️ Для получения информации о командах и их использовании "
            + "напиши</b> /help"
        )
        data.text = text

        await self.show_menu(data)

    async def show_menu(self, data: UserShowMenu):
        await self._bot.send_message(
            chat_id=data.chat_id,
            text=(data.text or "Меню"),
            reply_markup=start(data.is_admin),
        )

    async def inform_that_user_give_access(self, chat_id: int):
        text = "Вам выдали доступ к боту"
        await self._bot.send_message(chat_id=chat_id, text=text)

    async def user_not_found(self, chat_id: int):
        text = "Такой пользователь не найден, попросите его зайти в бота"
        await self._bot.send_message(
            chat_id=chat_id, text=text, reply_markup=start()
        )

    async def ask_to_enter_username(
        self, chat_id: int, message_id: Optional[str] = None
    ):
        text = 'Заполните поле "Имя пользователя" в настройках'
        args = {
            "chat_id": chat_id,
            "text": text,
        }
        if message_id is not None:
            args["reply_to_message_id"] = message_id

        await self._bot.send_message(**args)
