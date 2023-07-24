from typing import Optional
from chat_gpt.core.base.use_case import UseCase
from chat_gpt.core.exceptions import (
    MoreUserContextsFoundException,
)
from chat_gpt.core.protocols import UserContextGateway
from chat_gpt.core.dto import UserContextGetByFilters
from chat_gpt.core.entities import UserContext


class UserContextGetOneByFiltersUseCase(
    UseCase[UserContextGetByFilters, Optional[UserContext]]
):
    def __init__(
        self,
        user_context_gateway: UserContextGateway,
    ):
        self._user_context_gateway = user_context_gateway

    async def execute(
        self, data: UserContextGetByFilters
    ) -> Optional[UserContext]:
        user_contexts = await self._user_context_gateway.get_by_filters(data)
        if not user_contexts:
            return None
        if len(user_contexts) != 1:
            raise MoreUserContextsFoundException()
        return user_contexts[0]
