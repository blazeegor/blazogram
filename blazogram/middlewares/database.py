from typing import Union

from ..database.base import Database
from ..types import CallbackQuery, Message
from .base import BaseMiddleware


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, database: Database):
        self.database = database

    async def __call__(self,
                       handler: callable,
                       update: Union[Message, CallbackQuery],
                       data: dict):
        await self.database.add_user(user=update.from_user)
        data['database'] = self.database
        return await handler()