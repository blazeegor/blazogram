from .base import Database
from ..types.user import User

class MemoryDatabase(Database):
    def __init__(self):
        self.users: list[User] = []

    async def user_exists(self, user: User) -> bool:
        return user in self.users

    async def add_user(self, user: User) -> None:
        if not await self.user_exists(user):
            self.users.append(user)

    async def get_users(self) -> list[User]:
        return self.users.copy()
