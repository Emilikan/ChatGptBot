from pydantic import BaseModel
from chat_gpt.core.entities import UserId


class SendQuery(BaseModel):
    user_id: UserId
    query_text: str
