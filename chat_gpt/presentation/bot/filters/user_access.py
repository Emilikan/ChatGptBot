from typing import Dict
from aiogram.types import Message
from aiogram.filters import BaseFilter


class UserAccess(BaseFilter):
    async def __call__(
        self,
        message: Message,
        useful_data: Dict,
    ) -> bool:
        user = useful_data["user"]
        if user is None:
            return False
        return user.access
