from dataclasses import dataclass
from typing import Any

from .message import Message
from .user import User


@dataclass
class CallbackQuery:
    bot: Any
    id: int
    data: str
    from_user: User
    message: Message
    chat_instance: str = None

    async def answer(self, text: str = None, url: str = None, cache_time: int = None, show_alert: bool = False):
        return await self.bot.answer_callback_query(self.id, text, url, cache_time, show_alert)