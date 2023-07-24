from chat_gpt.core.base.use_case import UseCase
from chat_gpt.core.exceptions import (
    UserNotFoundException,
)
from chat_gpt.core.protocols import Commiter, UserGateway
from chat_gpt.core.dto import AdminCreate, UserGetByFilters


class AdminCreateUseCase(UseCase[AdminCreate, None]):
    def __init__(
        self,
        user_gateway: UserGateway,
        commiter: Commiter,
    ):
        self._user_gateway = user_gateway
        self._commiter = commiter

    async def execute(self, data: AdminCreate) -> None:
        users = await self._user_gateway.get_by_filters(
            UserGetByFilters(id=data.user_id)
        )
        if not users:
            raise UserNotFoundException
        user = users[0]
        user.is_admin = True

        await self._user_gateway.update(user)
        await self._commiter.commit()
