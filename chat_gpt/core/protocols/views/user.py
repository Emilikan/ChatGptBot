from typing import Protocol, Optional
from chat_gpt.core.dto import UserShowMenu


class UserView(Protocol):
    async def greeting(self, data: UserShowMenu):
        raise NotImplementedError

    async def show_menu(self, data: UserShowMenu):
        raise NotImplementedError

    async def inform_that_user_give_access(self, chat_id: int):
        raise NotImplementedError

    async def user_not_found(self, chat_id: int):
        raise NotImplementedError

    async def ask_to_enter_username(
        self, chat_id: int, message_id: Optional[str] = None
    ):
        raise NotImplementedError
