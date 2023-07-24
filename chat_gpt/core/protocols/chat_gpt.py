from typing import Protocol, List, Dict


class ChatGpt(Protocol):
    async def send_query(
        self, query_text: str, context=List[Dict[str, str]]
    ) -> str:
        raise NotImplementedError
