from .base import BaseFilter
from blazogram.types.objects.message import Message


class Command(BaseFilter):
    def __init__(self, command: str):
        self.command = '/' + command

    async def __check__(self, message: Message) -> bool:
        return message.text == self.command