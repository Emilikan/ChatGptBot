from chat_gpt.core.protocols import Commiter
from chat_gpt.infrastructure.storage.sqlalchemy.gateway import BaseGateway


class CommiterImp(BaseGateway, Commiter):
    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
