from typing import Callable, Awaitable, Any
from abc import ABC, abstractmethod


class BaseMiddleware(ABC):
    @abstractmethod
    async def __call__(self,
                       handler: Callable[[dict], Awaitable[Any]],
                       update,
                       data: dict) -> Any:
        pass