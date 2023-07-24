from typing import Optional
from pydantic import BaseModel
from chat_gpt.core.entities import UserId


class UserCreate(BaseModel):
    id: UserId
    name: Optional[str]
    number_requests: int = 0
    access: bool = False
    is_admin: bool = False


class UserGetByFilters(BaseModel):
    id: Optional[UserId] = None
    name: Optional[str] = None
    access: Optional[bool] = None
    is_admin: Optional[bool] = None


class UserGiveAccess(BaseModel):
    user_id: UserId


class UserRemoveAccess(BaseModel):
    user_id: UserId


class UserResetLimitRequests(BaseModel):
    ...


class UserShowMenu(BaseModel):
    chat_id: int
    text: str = ""
    is_admin: bool = False
