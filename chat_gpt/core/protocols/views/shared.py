from typing import Protocol


class SharedView(Protocol):
    async def error(self, chat_id: int, text: str = ""):
        raise NotImplementedError

    async def unresolved_group(self, chat_id: int):
        raise NotImplementedError
