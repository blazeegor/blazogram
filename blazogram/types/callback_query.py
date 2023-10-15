from .user import User
from .message import Message
from typing import Any
from dataclasses import dataclass


@dataclass
class CallbackQuery:
    bot: Any
    id: int
    data: str
    from_user: User
    message: Message
    chat_instance: str = None

    async def answer(self, text: str, show_alert: bool = False):
        return await self.bot.answer_callback_query(self.id, text=text, show_alert=show_alert)