from typing import Optional, List, Dict
from pydantic import BaseModel
from chat_gpt.core.entities import UserContextId, UserId


class UserContextCreate(BaseModel):
    user_id: UserId
    context: List[Dict[str, str]]


class UserContextGetByFilters(BaseModel):
    id: Optional[UserContextId] = None
    user_id: Optional[UserId] = None


class UserContextUpdate(BaseModel):
    user_id: UserId
    context: List[Dict[str, str]]


class UserContextDelete(BaseModel):
    user_id: UserId


class UserContextCleare(BaseModel):
    user_id: UserId


class UserContextCleareAll(BaseModel):
    ...


# class UserContextGetGroups(BaseModel):
#     user_id: UserContextId
#     is_chat_admin: Optional[bool] = None


# class UserContextShowMenu(BaseModel):
#     chat_id: int
#     text: str = ""
#     is_admin: bool = False
