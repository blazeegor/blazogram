from .telegram_update import TelegramUpdate, Handler
from ..middlewares.base import BaseMiddleware


class Router:
    def __init__(self):
        self.handlers: list[Handler] = []
        self.middlewares: list[BaseMiddleware] = []

        self.message = TelegramUpdate(router=self, update='message')
        self.callback_query = TelegramUpdate(router=self, update='callback_query')
        self.inline_query = TelegramUpdate(router=self, update='inline_query')

    def register_middleware(self, middleware: BaseMiddleware):
        self.middlewares.append(middleware)
