from .base import BaseMiddleware
from ..types import Message
from dataclasses import dataclass
from typing import Callable, Awaitable, Any
from datetime import datetime, timedelta


@dataclass(frozen=True)
class UserKey:
    chat_id: int
    user_id: int


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, delay: int = 2):
        self.delay = delay
        self.storage: dict[UserKey] = dict()

    async def __call__(self,
                       handler: Callable[[Message, dict], Awaitable[Any]],
                       update: Message,
                       data: dict) -> Any:
        key = UserKey(chat_id=update.chat.id, user_id=update.from_user.id)
        if key in self.storage.keys():
            if datetime.now() - self.storage[key] > timedelta(seconds=self.delay):
                return await handler(update, **data)
            else:
                return await update.answer('❗ Не так быстро.')
        else:
            self.storage[key] = datetime.now()
            return await handler(update, **data)