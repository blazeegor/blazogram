from .base import BaseFilter
from blazogram.types.objects.message import Message
from ..exceptions import FilterError


class Text(BaseFilter):
    def __init__(self, text: str = None, startswith: str = None, endswith: str = None):
        if text and startswith is None and endswith is None or startswith and text is None or endswith and text is None:
            self.text = text
            self.startswith = startswith
            self.endswith = endswith
        else:
            raise FilterError(message='Filter Text most have a one argument.')

    async def __check__(self, message: Message) -> bool:
        if self.text is not None:
            return message.text == self.text
        elif self.startswith is not None:
            return message.text.startswith(self.startswith)
        else:
            return message.text.endswith(self.endswith)