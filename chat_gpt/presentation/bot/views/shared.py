from .base import BaseView
from chat_gpt.core.protocols import SharedView

error_text_default = "Произошла ошибка, нажмите /start"


class SharedViewImpl(BaseView, SharedView):
    async def error(self, chat_id: int, text: str = error_text_default):
        await self._bot.send_message(chat_id=chat_id, text=text)

    async def unresolved_group(self, chat_id: int):
        text = "Эта группа не разрешена для работы"
        await self._bot.send_message(chat_id=chat_id, text=text)
