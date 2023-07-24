import g4f
from g4f.Provider import ChatgptAi
from typing import List, Dict
import traceback
import asyncio
import openai
from chat_gpt.config import Settings
from chat_gpt.core.protocols import ChatGpt


class ChatGptImpl(ChatGpt):
    def __init__(self, settings: Settings):
        self._settings = settings
        openai.api_key = settings.open_api_key

    async def send_query(
            self, query_text: str, context=List[Dict[str, str]]
    ) -> str:
        prompt_text = "\n".join(
            [f"{c['role']}: {c['content']}" for c in context]
        )
        context.append({"role": "user", "content": query_text})
        while True:
            try:
                response = g4f.ChatCompletion.create(
                    provider=ChatgptAi,
                    messages=[
                        {
                            "role": "system",
                            "content": "Ты полезный чат-бот ассистент по имени"
                                       + " Касандра",
                        },
                        {"role": "assistant", "content": prompt_text},
                        {"role": "user", "content": query_text},
                    ],
                    model=g4f.Model.gpt_4)
                message = response
                return message
            except Exception:
                traceback.print_exc()
                await asyncio.sleep(1)
