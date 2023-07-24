from chat_gpt.core.base.use_case import UseCase
from chat_gpt.core.exceptions import (
    GatewayException,
    UserAlreadyExistsException,
)
from chat_gpt.core.protocols import Commiter, UserGateway
from chat_gpt.core.dto import UserCreate
from chat_gpt.core.services import UserService
from chat_gpt.core.entities import User


class UserCreateUseCase(UseCase[UserCreate, None]):
    def __init__(
        self,
        user_service: UserService,
        user_gateway: UserGateway,
        commiter: Commiter,
    ):
        self._user_service = user_service
        self._user_gateway = user_gateway
        self._commiter = commiter

    async def execute(self, user_dto: UserCreate) -> User:
        user = self._user_service.create(user_dto)
        try:
            await self._user_gateway.create(user)
        except GatewayException as e:
            UserAlreadyExistsException(str(e))
        await self._commiter.commit()
        return user
