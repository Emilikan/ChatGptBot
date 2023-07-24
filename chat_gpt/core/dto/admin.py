from pydantic import BaseModel
from chat_gpt.core.entities import UserId


class AdminCreate(BaseModel):
    user_id: UserId


class AdminDelete(BaseModel):
    user_id: UserId
