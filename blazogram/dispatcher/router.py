from .telegram_update import TelegramUpdate, Handler
from ..middlewares.base import BaseMiddleware

class Router:
    def __init__(self):
        self.handlers: list[Handler] = []
        self.message = TelegramUpdate(router=self, update='message')
        self.callback_query = TelegramUpdate(router=self, update='callback_query')

    def register_middleware(self, middleware: BaseMiddleware) -> None:
        self.message.register_middleware(middleware)
        self.callback_query.register_middleware(middleware)
