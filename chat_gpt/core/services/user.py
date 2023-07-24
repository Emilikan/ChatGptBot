from chat_gpt.core.dto import UserCreate
from chat_gpt.core.entities import User


class UserService:
    def create(self, data: UserCreate) -> User:
        return User(
            id=data.id,
            name=data.name,
            number_requests=data.number_requests,
            access=data.access,
            is_admin=data.is_admin,
        )
