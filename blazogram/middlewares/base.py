from abc import ABC, abstractmethod


class BaseMiddleware(ABC):
    @abstractmethod
    async def __call__(self,
                       handler: callable,
                       update,
                       data: dict):
        pass