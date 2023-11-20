from abc import ABC, abstractmethod
from typing import Callable, Any, Awaitable


class BaseMiddleware(ABC):
    @abstractmethod
    async def __call__(
        self, handler: Callable[..., Awaitable[Any]], update: Any, data: dict[str, Any]
    ):
        pass
