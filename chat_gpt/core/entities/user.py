from dataclasses import dataclass
from typing import NewType, Optional


UserId = NewType("UserId", int)


@dataclass
class User:
    id: Optional[UserId]
    name: Optional[str]
    number_requests: int
    access: bool
    is_admin: bool
