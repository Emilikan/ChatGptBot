from typing import Protocol


class AdminView(Protocol):
    async def greeting(self, chat_id: int, is_main_admin: bool = False):
        raise NotImplementedError

    async def group_created(self, chat_id: int):
        raise NotImplementedError

    async def user_not_found(self, chat_id: int):
        raise NotImplementedError

    async def inform_that_user_become_admin(self, chat_id: int):
        raise NotImplementedError

    async def inform_that_user_stopped_being_admin(self, chat_id: int):
        raise NotImplementedError
