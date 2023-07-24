from typing import List
from sqlalchemy import select, update
from chat_gpt.infrastructure.storage.sqlalchemy.gateway import BaseGateway
from chat_gpt.core.protocols import UserGateway
from chat_gpt.core.dto import UserGetByFilters
from chat_gpt.core.entities import User


class UserGatewayImpl(BaseGateway, UserGateway):
    async def create(self, user: User) -> None:
        self._session.add(user)
        await self._try_exc_flush()

    async def get_by_filters(self, data: UserGetByFilters) -> List[User]:
        stmt = select(User)
        if data.id:
            stmt = stmt.where(User.id == data.id)  # type: ignore
        if data.name:
            stmt = stmt.where(User.name == data.name)  # type: ignore
        if data.access:
            stmt = stmt.where(User.access == data.access)  # type: ignore
        if data.is_admin:
            stmt = stmt.where(User.is_admin == data.is_admin)  # type: ignore
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def update(self, user: User) -> None:
        await self._session.execute(
            update(User)
            .where(User.id == user.id)  # type: ignore
            .values(
                name=user.name,
                number_requests=user.number_requests,
                is_admin=user.is_admin,
            )
        )

    async def reser_limit_requests(self) -> None:
        await self._session.execute(
            update(User)
            .values(
                number_requests=0,
            )
        )
