from ..filters.base import BaseFilter
from ..middlewares.base import BaseMiddleware
from dataclasses import dataclass


@dataclass
class Handler:
    func: callable
    update: str
    filters: list
    middlewares: list


class TelegramUpdate:
    def __init__(self, router, update: str):
        self.router = router
        self.update = update
        self._filters = []
        self._middlewares = []

    def register_middleware(self, middleware: BaseMiddleware):
        self._middlewares.append(middleware)

    def register(self, handler: callable, *filters: BaseFilter):
        filters = list(filters)
        filters.extend(self._filters)
        self.router.handlers.append(Handler(func=handler, update=self.update, filters=filters, middlewares=self._middlewares))

    def filter(self, filter: BaseFilter):
        self._filters.append(filter)

    def __call__(self, *filters: BaseFilter):
        def wrapper(func):
            self.register(func, *filters)
        return wrapper
