from .base import BaseMiddleware
from ..database.base import Database
from ..types import Message, CallbackQuery
from typing import Union

class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, database: Database):
        self.database = database

    async def __call__(self,
                       handler: callable,
                       update: Union[Message, CallbackQuery],
                       data: dict) -> None:
        await self.database.add_user(user=update.from_user)
        data['database'] = self.database
        return await handler()
