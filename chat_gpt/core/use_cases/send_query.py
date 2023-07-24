from chat_gpt.core.base.use_case import UseCase
from chat_gpt.core.exceptions import (
    UserNotFoundException,
)
from chat_gpt.config import Settings
from chat_gpt.core.protocols import (
    Commiter,
    UserContextGateway,
    UserGateway,
    ChatGpt,
)
from chat_gpt.core.dto import (
    SendQuery,
    UserContextGetByFilters,
    UserGetByFilters,
)
from chat_gpt.core.entities import UserContext, User


class SendQueryUseCase(UseCase[SendQuery, str]):
    def __init__(
        self,
        chat_gpt: ChatGpt,
        user_context_gateway: UserContextGateway,
        user_gateway: UserGateway,
        commiter: Commiter,
        settings: Settings,
    ):
        self._chat_gpt = chat_gpt
        self._user_context_gateway = user_context_gateway
        self._user_gateway = user_gateway
        self._commiter = commiter
        self._settings = settings

    async def execute(self, data: SendQuery) -> str:
        user_context = await self._get_user_context(data)
        user = await self._get_user(data)

        context = user_context.context
        answer = await self._chat_gpt.send_query(data.query_text, context)
        context.append({"role": "user", "content": data.query_text})
        context.append({"role": "assistant", "content": answer})
        context = context[-self._settings.context_message_limit :]

        user_context.context = context
        await self._user_context_gateway.update(user_context)
        user.number_requests += 1
        await self._user_gateway.update(user)
        await self._commiter.commit()

        return answer

    async def _get_user_context(self, data: SendQuery) -> UserContext:
        user_contexts = await self._user_context_gateway.get_by_filters(
            UserContextGetByFilters(user_id=data.user_id)
        )
        if not user_contexts:
            user_context = UserContext(
                id=None, user_id=data.user_id, context=[]
            )
            await self._user_context_gateway.create(user_context)
        else:
            user_context = user_contexts[0]
        return user_context

    async def _get_user(self, data: SendQuery) -> User:
        users = await self._user_gateway.get_by_filters(
            UserGetByFilters(id=data.user_id)
        )
        if not users:
            raise UserNotFoundException()
        return users[0]
