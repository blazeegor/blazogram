from .methods import Methods
from .types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup
from typing import Union, Literal
from dataclasses import dataclass


@dataclass
class Bot:
    def __init__(self, token: str, parse_mode: Literal['HTML', 'MARKDOWN'] = 'None'):
        self.token = token
        self.parse_mode = parse_mode
        self.methods = Methods(token)

    async def send_message(self, chat_id: int, text: str, parse_mode: Literal['HTML', 'MARKDOWN', 'None'] = 'None', reply_markup: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove] = ReplyKeyboardMarkup()) -> Message:
        return await self.methods.SendMessage(chat_id, text, reply_markup.reply_markup, parse_mode)

    async def get_me(self):
        return await self.methods.GetMe()

    async def get_updates(self):
        return await self.methods.GetUpdates()

    async def skip_updates(self):
        return await self.methods.SkipUpdates()

    async def answer_callback_query(self, callback_query_id: int, text: str, show_alert: bool = False):
        return await self.methods.AnswerCallbackQuery(callback_query_id, text, show_alert)

    async def delete_message(self, chat_id: int, message_id: int):
        return await self.methods.DeleteMessage(chat_id, message_id)

    async def get_chat(self, chat_id: int):
        return await self.methods.GetChat(chat_id)