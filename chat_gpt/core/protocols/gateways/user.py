from typing import Protocol, List
from chat_gpt.core.dto import UserGetByFilters
from chat_gpt.core.entities import User


class UserGateway(Protocol):
    async def create(self, user: User) -> None:
        raise NotImplementedError

    async def get_by_filters(self, data: UserGetByFilters) -> List[User]:
        raise NotImplementedError

    async def update(self, user: User) -> None:
        raise NotImplementedError

    async def reser_limit_requests(self) -> None:
        raise NotImplementedError
