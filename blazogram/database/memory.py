from .base import Database
from ..types.user import User


class MemoryDatabase(Database):
    def __init__(self):
        self.users: list[User] = []

    async def user_exist(self, user: User) -> bool:
        users = await self.get_users()
        return user in users

    async def add_user(self, user: User):
        if await self.user_exist(user=user) is False:
            self.users.append(user)

    async def get_users(self) -> list[User]:
        return self.users
