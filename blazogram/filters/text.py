from .base import BaseFilter
from ..types.message import Message
from ..exceptions import FilterError


class Text(BaseFilter):
    def __init__(self, text: str = None, startswith: str = None, endswith: str = None):
        if text and (startswith or endswith):
            raise FilterError(message='Filter Text most have a only one argument.')

        self.text = text
        self.startswith = startswith
        self.endswith = endswith

    async def __check__(self, message: Message) -> bool:
        if self.text is not None:
            return message.text == self.text
        elif self.startswith is not None:
            return message.text.startswith(self.startswith)
        else:
            return message.text.endswith(self.endswith)