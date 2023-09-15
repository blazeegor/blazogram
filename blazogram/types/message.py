from .objects import Chat, User, PhotoSize, InputFile
from .reply_keyboard import ReplyKeyboardMarkup, ReplyKeyboardRemove
from .inline_keyboard import InlineKeyboardMarkup
from typing import Union, Literal


class Message:
    def __init__(self, bot, message_id: int, chat: Chat, user: User, photo: list[PhotoSize] = None, text: str = None, caption: str = None):
        self.bot = bot
        self.message_id = message_id
        self.from_user = user
        self.chat = chat
        self.text = text
        self.caption = caption
        self.photo = photo

    async def answer(self, text: str, parse_mode: Literal['HTML', 'MARKDOWN'] = None, reply_markup: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove] = ReplyKeyboardMarkup()):
        return await self.bot.send_message(chat_id=self.chat.id, text=text, parse_mode=parse_mode, reply_markup=reply_markup)

    async def answer_photo(self, photo: Union[InputFile, str], caption: str = None, parse_mode: Literal['HTML', 'MARKDOWN'] = None, reply_markup: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove] = ReplyKeyboardMarkup()):
        return await self.bot.send_photo(chat_id=self.chat.id, photo=photo, caption=caption, parse_mode=parse_mode, reply_markup=reply_markup)

    async def delete(self):
        return await self.bot.delete_message(self.chat.id, self.message_id)