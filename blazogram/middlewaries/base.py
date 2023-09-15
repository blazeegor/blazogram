from typing import Callable, Awaitable, Any


class BaseMiddleware:
    async def __call__(self,
                       handler: Callable[[dict], Awaitable[Any]],
                       update,
                       data: dict) -> Any:
        pass