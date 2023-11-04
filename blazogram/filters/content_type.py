from typing import Literal

from ..types import Message
from .base import BaseFilter


class ContentType(BaseFilter):
    def __init__(self, content_type: Literal['text', 'photo']):
        self.content_type = content_type

    async def __check__(self, message: Message):
        if self.content_type == 'text':
            return message.text is not None
        elif self.content_type == 'photo':
            return message.photo is not None