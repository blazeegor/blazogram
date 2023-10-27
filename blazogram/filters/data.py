from .base import BaseFilter
from ..types.callback_query import CallbackQuery
from ..exceptions import FilterError

class Data(BaseFilter):
    def __init__(self, data: str = None, starts_with: str = None, ends_with: str = None):
        if data and (starts_with or ends_with):
            self.data = data
            self.starts_with = starts_with
            self.ends_with = ends_with
        else:
            raise FilterError(message='Filter Data must have exactly one argument.')

    async def __check__(self, callback_query: CallbackQuery) -> bool:
        if self.data is not None:
            return callback_query.data == self.data
        elif self.starts_with is not None:
            return callback_query.data.startswith(self.starts_with)
        else:
            return callback_query.data.endswith(self.ends_with)
