from typing import List
from sqlalchemy import select, update, delete
from chat_gpt.infrastructure.storage.sqlalchemy.gateway import BaseGateway
from chat_gpt.core.protocols import UserContextGateway
from chat_gpt.core.dto import UserContextGetByFilters
from chat_gpt.core.entities import UserContext, UserId


class UserContextGatewayImpl(BaseGateway, UserContextGateway):
    async def create(self, user_context: UserContext):
        self._session.add(user_context)
        await self._try_exc_flush()

    async def get_by_filters(
        self, filters: UserContextGetByFilters
    ) -> List[UserContext]:
        stmt = select(UserContext)
        if filters.id:
            stmt = stmt.where(UserContext.id == filters.id)  # type: ignore
        if filters.user_id:
            stmt = stmt.where(UserContext.user_id == filters.user_id)  # type: ignore # noqa
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def update(self, user_context: UserContext):
        await self._session.execute(
            update(UserContext)
            .where(UserContext.id == user_context.id)  # type: ignore
            .values(
                user_id=user_context.user_id,
                context=user_context.context,
            )
        )

    async def cleare_all_contexts(self):
        await self._session.execute(
            update(UserContext).values(
                context=[],
            )
        )

    async def delete(self, user_context_id: UserId):
        await self._session.execute(
            delete(UserContext).where(
                UserContext.id == user_context_id  # type: ignore
            )
        )
