from .methods import Methods
from ..types.keyboard.reply_keyboard import ReplyKeyboardMarkup
from ..types.keyboard.inline_keyboard import InlineKeyboardMarkup
from typing import Union


class Bot:
    def __init__(self, token: str):
        self.token = token
        self.methods = Methods(token)

    async def send_message(self, chat_id: int, text: str, reply_markup: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup] = ReplyKeyboardMarkup()):
        return await self.methods.SendMessage(chat_id, text, reply_markup.reply_markup)

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