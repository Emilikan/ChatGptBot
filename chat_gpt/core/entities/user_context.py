from dataclasses import dataclass
from typing import NewType, Optional, Dict, List
from .user import UserId


UserContextId = NewType("UserContextId", int)


@dataclass
class UserContext:
    id: Optional[UserContextId]
    user_id: UserId
    context: List[Dict[str, str]]
