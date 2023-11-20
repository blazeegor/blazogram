from abc import ABC, abstractmethod


class Database(ABC):
    @abstractmethod
    async def add_user(self, user):
        pass

    @abstractmethod
    async def get_users(self) -> list:
        pass
