import enum
from typing import Sequence, Optional, Any, Type
from di.executors import AsyncExecutor
from di.api.scopes import Scope
from di import Container, ScopeState
from di.dependent import Dependent
from di.api.providers import DependencyProvider


class DIContainer:
    def __init__(self, container: Container, scopes: Sequence[Scope]):
        self._container = container
        self._executor = AsyncExecutor()
        self._cache = {}  # type: ignore
        self._scopes = scopes

    async def provider(
        self,
        type_: Type,
        state: ScopeState,
        scope: Scope,
        values: dict[DependencyProvider, Any] = {},
    ):
        from_cache = self._cache.get(type_)
        if from_cache:
            solved = from_cache  # type: ignore
        else:
            solved = self._container.solve(
                Dependent(type_, scope=scope), self._scopes
            )
            self._cache[type_] = solved
        return await solved.execute_async(
            executor=self._executor, state=state, values=values
        )

    def enter_scope(
        self,
        scope: Scope,
        state: Optional[ScopeState] = None,
    ):
        return self._container.enter_scope(scope, state)


class DIScope(enum.Enum):
    APP = "app"
    REQUEST = "request"
