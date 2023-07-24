from chat_gpt.core.dto import UserContextCreate
from chat_gpt.core.entities import UserContext


class UserContextService:
    def create(self, data: UserContextCreate) -> UserContext:
        return UserContext(
            id=None,
            user_id=data.user_id,
            context=data.context,
        )
