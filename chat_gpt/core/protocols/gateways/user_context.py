from typing import List
from typing import Protocol
from chat_gpt.core.dto import UserContextGetByFilters
from chat_gpt.core.entities import UserContext, UserId


class UserContextGateway(Protocol):
    async def create(self, user_context: UserContext):
        raise NotImplementedError

    async def get_by_filters(
        self, filters: UserContextGetByFilters
    ) -> List[UserContext]:
        raise NotImplementedError

    async def update(self, user_context: UserContext):
        raise NotImplementedError

    async def cleare_all_contexts(self):
        raise NotImplementedError

    async def delete(self, user_id: UserId):
        raise NotImplementedError
