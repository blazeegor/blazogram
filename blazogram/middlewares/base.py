from abc import ABC, abstractmethod
from typing import Callable, Any, Dict

class BaseMiddleware(ABC):
    @abstractmethod
    async def __call__(self,
                       handler: Callable[..., Any],
                       update: Any,
                       data: Dict[str, Any]) -> None:
        pass
