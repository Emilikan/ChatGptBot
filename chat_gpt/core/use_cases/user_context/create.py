from chat_gpt.core.base.use_case import UseCase
from chat_gpt.core.exceptions import (
    GatewayException,
    UserContextAlreadyExistsException,
)
from chat_gpt.core.protocols import Commiter, UserContextGateway
from chat_gpt.core.dto import UserContextCreate
from chat_gpt.core.services import UserContextService
from chat_gpt.core.entities import UserContext


class UserContextCreateUseCase(UseCase[UserContextCreate, UserContext]):
    def __init__(
        self,
        user_context_service: UserContextService,
        user_context_gateway: UserContextGateway,
        commiter: Commiter,
    ):
        self._user_context_service = user_context_service
        self._user_context_gateway = user_context_gateway
        self._commiter = commiter

    async def execute(self, data: UserContextCreate) -> UserContext:
        user_context = self._user_context_service.create(data)
        try:
            await self._user_context_gateway.create(user_context)
        except GatewayException as e:
            UserContextAlreadyExistsException(str(e))
        await self._commiter.commit()
        return user_context
