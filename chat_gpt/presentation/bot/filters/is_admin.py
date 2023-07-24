from typing import Dict
from aiogram.types import Message
from aiogram.filters import BaseFilter


class IsAdmin(BaseFilter):
    async def __call__(
        self,
        message: Message,
        useful_data: Dict,
    ) -> bool:
        user = useful_data["user"]
        return user.is_admin
