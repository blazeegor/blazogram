from blazogram.filters.base import BaseFilter
from blazogram.types.telegram_update import TelegramUpdate


class Router:
    def __init__(self):
        self.handlers = []
        self.message = TelegramUpdate(router=self, update='message')
        self.callback_query = TelegramUpdate(router=self, update='callback_query')

    # def message(self, *filters: BaseFilter):
    #     def wrapper(func):
    #         self.handlers.append((func, 'message', filters,))
    #     return wrapper
    #
    # def callback_query(self, *filters: BaseFilter):
    #     def wrapper(func):
    #         self.handlers.append((func, 'callback_query', filters,))
    #     return wrapper