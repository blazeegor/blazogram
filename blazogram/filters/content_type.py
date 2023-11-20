from .base import BaseFilter
from ..types import Message
from ..enums import ContentTypes


class ContentType(BaseFilter):
    def __init__(self, content_type: ContentTypes):
        self.content_type = content_type.name

    async def __check__(self, message: Message):
        if self.content_type == "text":
            return message.text is not None
        elif self.content_type == "photo":
            return message.photo is not None
