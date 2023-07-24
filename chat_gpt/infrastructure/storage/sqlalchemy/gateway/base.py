from typing import Protocol
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from chat_gpt.core.exceptions import GatewayException


class Gateway(Protocol):
    def __init__(self, session: AsyncSession) -> None:
        raise NotImplementedError


class BaseGateway(Gateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def _try_exc_flush(self):
        try:
            await self._session.flush()
            await self._session.commit()
        except IntegrityError as e:
            await self._session.rollback()
            raise GatewayException(str(e))
