from typing import Optional
from chat_gpt.core.base.use_case import UseCase
from chat_gpt.core.exceptions import (
    MoreUsersFoundException,
)
from chat_gpt.core.protocols import UserGateway
from chat_gpt.core.dto import UserGetByFilters
from chat_gpt.core.entities import User


class UserGetOneByFiltersUseCase(UseCase[UserGetByFilters, Optional[User]]):
    def __init__(
        self,
        user_gateway: UserGateway,
    ):
        self._user_gateway = user_gateway

    async def execute(self, data: UserGetByFilters) -> Optional[User]:
        users = await self._user_gateway.get_by_filters(data)
        if not users:
            return None
        if len(users) != 1:
            raise MoreUsersFoundException()
        return users[0]
