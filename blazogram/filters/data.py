from .base import BaseFilter
from ..types.callback_query import CallbackQuery
from ..exceptions import FilterError


class Data(BaseFilter):
    def __init__(self, data: str = None, startswith: str = None, endswith: str = None):
        if data and (startswith or endswith):
            raise FilterError(message='Filter Data most have a only one argument.')

        self.data = data
        self.startswith = startswith
        self.endswith = endswith

    async def __check__(self, callback_query: CallbackQuery) -> bool:
        if self.data is not None:
            return callback_query.data == self.data
        elif self.startswith is not None:
            return callback_query.data.startswith(self.startswith)
        elif self.endswith is not None:
            return callback_query.data.endswith(self.endswith)