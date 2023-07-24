from typing import Protocol, Type, TypeVar, Any
from di import ScopeState
from chat_gpt.presentation.di import DIContainer, DIScope

T = TypeVar("T")


class IoC(Protocol):
    def set_scope_and_state(self, di_state: ScopeState, di_scope: DIScope):
        raise NotImplementedError

    async def provider(self, type_: Type[Any]) -> Any:
        raise NotImplementedError


class IoCImpl(IoC):
    def __init__(
        self,
        di_container: DIContainer,
    ):
        self._di_container = di_container

    def set_scope_and_state(self, di_state: ScopeState, di_scope: DIScope):
        self._di_scope = di_scope
        self._di_state = di_state

    async def provider(self, type_: Type[Any]) -> Any:
        dependens = await self._di_container.provider(
            type_, self._di_state, self._di_scope
        )
        return dependens
