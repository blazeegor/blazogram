from .base import BaseMiddleware
from ..types import Message
from dataclasses import dataclass
from typing import Callable, Awaitable, Any
from datetime import datetime, timedelta

@dataclass(frozen=True)
class UserKey:
    chat_id: int
    user_id: int

@dataclass(frozen=True)
class DataKey:
    date: datetime
    is_message: bool

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, delay: int = 3, message: str = '❗️ Не так быстро.'):
        self.delay = delay
        self.message = message
        self.storage: dict[UserKey, DataKey] = {}

    async def __call__(self,
                       handler: Callable[..., Awaitable[Any]],
                       update: Message,
                       data: dict) -> Any:
        key = UserKey(chat_id=update.chat.id, user_id=update.from_user.id)
        if key in self.storage:
            if datetime.now() - self.storage[key].date > timedelta(seconds=self.delay):
                self.storage.pop(key)
                return await handler()
            data_key = self.storage[key].replace(is_message=False)
            self.storage[key] = data_key
            return await update.answer(text=self.message)
        else:
            data_key = DataKey(date=datetime.now(), is_message=True)
            self.storage[key] = data_key
            return await handler()
