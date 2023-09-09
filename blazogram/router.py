from .filters.base import BaseFilter


class Router:
    def __init__(self):
        self.handlers = []

    def message(self, *filters: BaseFilter):
        def wrapper(func):
            self.handlers.append((func, 'message', filters,))
        return wrapper

    def callback_query(self, *filters: BaseFilter):
        def wrapper(func):
            self.handlers.append((func, 'callback_query', filters,))
        return wrapper