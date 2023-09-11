from .base import BaseFilter
from ..types.message import Message


class Text(BaseFilter):
    def __init__(self, text: str = None, startswith: str = None, endswith: str = None):
        if text is not None and startswith is None and endswith is None or startswith is not None and text is None or endswith is not None and text is None:
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