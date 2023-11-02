from .base import BaseFilter
from ..types.message import Message


class ChatTypeFilter(BaseFilter):
    def __init__(self, chat_type: list[str] | str):
        self.chat_type = chat_type if isinstance(chat_type, list) else [chat_type]

    async def __check__(self, message: Message) -> bool:
        return message.chat.type in self.chat_type