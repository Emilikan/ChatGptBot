from typing import Protocol


class Commiter(Protocol):
    async def commit(self):
        raise NotImplementedError

    async def rollback(self):
        raise NotImplementedError
