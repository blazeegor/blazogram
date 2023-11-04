from typing import Union

from ..types import CallbackQuery, Message
from .base import BaseFilter


class UserFilter(BaseFilter):
    def __init__(self, users: list[int] | int):
        self.users = users if isinstance(users, list) else [users]

    async def __check__(self, update: Union[Message, CallbackQuery]) -> bool:
        return update.from_user.id in self.users