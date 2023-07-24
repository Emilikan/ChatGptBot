from chat_gpt.core.base.use_case import UseCase
from chat_gpt.core.protocols import Commiter, UserContextGateway
from chat_gpt.core.dto import UserContextDelete


class UserContextDeleteUseCase(UseCase[UserContextDelete, None]):
    def __init__(
        self,
        user_context_gateway: UserContextGateway,
        commiter: Commiter,
    ):
        self._user_context_gateway = user_context_gateway
        self._commiter = commiter

    async def execute(self, data: UserContextDelete) -> None:
        await self._user_context_gateway.delete(data.user_id)
        await self._commiter.commit()
