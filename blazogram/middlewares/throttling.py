from .base import BaseMiddleware
from ..types import Message
from dataclasses import dataclass
from typing import Callable, Awaitable, Any
from datetime import datetime, timedelta


@dataclass(frozen=True)
class UserKey:
    chat_id: int
    user_id: int


@dataclass
class DataKey:
    date: datetime
    is_message: bool


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, delay: int = 3, message: str = '❗ Не так быстро.'):
        self.delay = delay
        self.message = message
        self.storage: dict[UserKey, DataKey] = dict()

    async def __call__(self,
                       handler: callable,
                       update: Message,
                       data: dict) -> Any:
        key = UserKey(chat_id=update.chat.id, user_id=update.from_user.id)
        if key in self.storage.keys():
            if datetime.now() - self.storage[key].date > timedelta(seconds=self.delay):
                self.storage.pop(key)
                return await handler()
            else:
                if self.storage[key].is_message is True:
                    self.storage[key].is_message = False
                    return await update.answer(text=self.message)
        else:
            self.storage[key] = DataKey(date=datetime.now(), is_message=True)
            return await handler()