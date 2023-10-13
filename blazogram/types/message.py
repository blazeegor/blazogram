from ..types.objects import Chat, User
from ..types.documents_types import PhotoSize
from .input_file import InputFile
from blazogram.types.reply_keyboard import ReplyKeyboardMarkup, ReplyKeyboardRemove
from blazogram.types.inline_keyboard import InlineKeyboardMarkup
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

    async def answer(self, text: str, parse_mode: str = None, reply_markup: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove] = ReplyKeyboardMarkup()):
        return await self.bot.send_message(chat_id=self.chat.id, text=text, parse_mode=parse_mode, reply_markup=reply_markup)

    async def answer_photo(self, photo: Union[InputFile, str], caption: str = None, parse_mode: Literal['HTML', 'MARKDOWN'] = None, reply_markup: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove] = ReplyKeyboardMarkup()):
        return await self.bot.send_photo(chat_id=self.chat.id, photo=photo, caption=caption, parse_mode=parse_mode, reply_markup=reply_markup)

    async def delete(self):
        return await self.bot.delete_message(chat_id=self.chat.id, message_id=self.message_id)

    async def edit_text(self, text: str, reply_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(), parse_mode: str = None):
        return await self.bot.edit_message_text(chat_id=self.chat.id, text=text, message_id=self.message_id, parse_mode=parse_mode, reply_markup=reply_markup)