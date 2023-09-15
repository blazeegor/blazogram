from ..filters.base import BaseFilter
from ..middlewaries.base import BaseMiddleware


class TelegramUpdate:
    def __init__(self, router, update: str):
        self.router = router
        self.update = update

    def register_middleware(self, middleware: BaseMiddleware):
        handlers = [hand for hand in self.router.handlers]
        for handler in self.router.handlers:
            if handler[1] == self.update:
                handlers.remove(handler)
                handlers.append((handler[0], self.update, handler[2], middleware,))
        self.router.handlers = handlers

    def register(self, handler: callable, *filters: BaseFilter):
        self.router.handlers.append((handler, self.update, filters,))

    def __call__(self, *filters: BaseFilter):
        def wrapper(func):
            self.router.handlers.append((func, self.update, filters,))
        return wrapper