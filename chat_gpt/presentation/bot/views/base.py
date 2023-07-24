from abc import ABC
from aiogram import Bot


class BaseView(ABC):
    def __init__(self, bot: Bot):
        self._bot = bot
