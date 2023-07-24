from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from pydantic import BaseModel

DtoType = TypeVar("DtoType", bound=BaseModel)
ReturnType = TypeVar("ReturnType")


class UseCase(ABC, Generic[DtoType, ReturnType]):
    @abstractmethod
    async def execute(self, obj: DtoType) -> ReturnType:
        raise NotImplementedError
