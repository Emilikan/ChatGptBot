from typing import List
from chat_gpt.core.base.use_case import UseCase
from chat_gpt.core.protocols import UserContextGateway
from chat_gpt.core.dto import UserContextGetByFilters
from chat_gpt.core.entities import UserContext


class UserContextGetByFiltersUseCase(
    UseCase[UserContextGetByFilters, List[UserContext]]
):
    def __init__(
        self,
        user_gateway: UserContextGateway,
    ):
        self._user_gateway = user_gateway

    async def execute(
        self, data: UserContextGetByFilters
    ) -> List[UserContext]:
        users = await self._user_gateway.get_by_filters(data)
        return users
