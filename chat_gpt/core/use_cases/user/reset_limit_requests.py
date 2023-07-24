from chat_gpt.core.base.use_case import UseCase
from chat_gpt.core.protocols import Commiter, UserGateway
from chat_gpt.core.dto import UserResetLimitRequests


class UserResetLimitRequestsUseCase(UseCase[UserResetLimitRequests, None]):
    def __init__(
        self,
        user_gateway: UserGateway,
        commiter: Commiter,
    ):
        self._user_gateway = user_gateway
        self._commiter = commiter

    async def execute(self, data: UserResetLimitRequests) -> None:
        await self._user_gateway.reser_limit_requests()
        await self._commiter.commit()
