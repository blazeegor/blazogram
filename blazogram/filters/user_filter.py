from .base import BaseFilter
from ..types import Message, CallbackQuery
from typing import Union


class UserFilter(BaseFilter):
    def __init__(self, users: list[int] | int):
        self.users = users if isinstance(users, list) else [users]

    async def __check__(self, update: Union[Message, CallbackQuery]) -> bool:
        return update.from_user.id in self.users