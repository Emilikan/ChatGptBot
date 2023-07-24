from typing import Dict
from aiogram.types import Message
from aiogram.filters import BaseFilter
from chat_gpt.config import Settings


class IsMainAdmin(BaseFilter):
    async def __call__(
        self, message: Message, useful_data: Dict, settings: Settings
    ) -> bool:
        user = useful_data["user"]
        return user.id == settings.main_admin
