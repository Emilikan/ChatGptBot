from .base import BaseView
from chat_gpt.core.protocols import AdminView
from chat_gpt.presentation.bot.keyboards.default.user import (
    start as user_start,
)
from chat_gpt.presentation.bot.keyboards.default.admin import start


class AdminViewImpl(BaseView, AdminView):
    async def greeting(self, chat_id: int, is_main_admin: bool = False):
        text = "Меню админа"
        await self._bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=start(is_main_admin=is_main_admin),
        )

    async def group_created(self, chat_id: int):
        text = "Группа стала разрешена для работы"
        await self._bot.send_message(chat_id=chat_id, text=text)

    async def user_not_found(self, chat_id: int):
        text = "Такой пользователь не найден, попросите его зайти в бота"
        await self._bot.send_message(
            chat_id=chat_id, text=text, reply_markup=start()
        )

    async def inform_that_user_become_admin(self, chat_id: int):
        text = "Вас сделали администратором, нажмите /start"
        await self._bot.send_message(chat_id=chat_id, text=text)

    async def inform_that_user_stopped_being_admin(self, chat_id: int):
        text = "Вас удалили из администраторов"
        await self._bot.send_message(
            chat_id=chat_id, text=text, reply_markup=user_start()
        )
