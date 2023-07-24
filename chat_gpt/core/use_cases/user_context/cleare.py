from chat_gpt.core.base.use_case import UseCase
from chat_gpt.core.exceptions import (
    UserContextNotFoundException,
)
from chat_gpt.core.protocols import Commiter, UserContextGateway
from chat_gpt.core.dto import UserContextCleare, UserContextGetByFilters


class UserContextCleareUseCase(UseCase[UserContextCleare, None]):
    def __init__(
        self,
        user_context_gateway: UserContextGateway,
        commiter: Commiter,
    ):
        self._user_context_gateway = user_context_gateway
        self._commiter = commiter

    async def execute(self, data: UserContextCleare) -> None:
        user_contexts = await self._user_context_gateway.get_by_filters(
            UserContextGetByFilters(user_id=data.user_id)
        )
        if not user_contexts:
            raise UserContextNotFoundException()
        user_context = user_contexts[0]

        user_context.context = []

        await self._user_context_gateway.update(user_context)

        await self._commiter.commit()
