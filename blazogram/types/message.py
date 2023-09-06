from ..types.user import User
from ..types.chat import Chat
from ..types.keyboard.reply_keyboard import ReplyKeyboardMarkup
from ..types.keyboard.inline_keyboard import InlineKeyboardMarkup
from typing import Union


class Message:
    def __init__(self, bot, message_id: int, text: str, chat: Chat, user: User):
        self.message_id = message_id
        self.bot = bot
        self.chat_id = chat.id
        self.from_user = User(id=user.id, first_name=user.first_name, username=user.username)
        self.chat = Chat(id=chat.id, first_name=chat.first_name, username=chat.username)
        self.text = text

    async def answer(self, text: str, reply_markup: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup] = ReplyKeyboardMarkup()):
        return await self.bot.send_message(chat_id=self.chat_id, text=text, reply_markup=reply_markup)

    async def delete(self):
        return await self.bot.delete_message(self.chat_id, self.message_id)