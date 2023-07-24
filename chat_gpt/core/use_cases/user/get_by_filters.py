from typing import List
from chat_gpt.core.base.use_case import UseCase
from chat_gpt.core.protocols import UserGateway
from chat_gpt.core.dto import UserGetByFilters
from chat_gpt.core.entities import User


class UserGetByFiltersUseCase(UseCase[UserGetByFilters, List[User]]):
    def __init__(
        self,
        user_gateway: UserGateway,
    ):
        self._user_gateway = user_gateway

    async def execute(self, data: UserGetByFilters) -> List[User]:
        users = await self._user_gateway.get_by_filters(data)
        return users
