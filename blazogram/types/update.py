from .message import Message
from .callback_query import CallbackQuery
from dataclasses import dataclass


@dataclass
class Update:
    update_id: int
    update: str
    message: Message = None
    edited_message: Message = None
    channel_post: Message = None
    edited_channel_post: Message = None
    callback_query: CallbackQuery = None
