from ..types.chat import Chat
from ..types.photo import PhotoSize
from ..types.user import User
from .input_file import InputFile
from blazogram.types.reply_keyboard import ReplyKeyboardMarkup, ReplyKeyboardRemove
from blazogram.types.inline_keyboard import InlineKeyboardMarkup
from typing import Union, Literal, Any
from dataclasses import dataclass


@dataclass
class Message:
    bot: Any
    message_id: int
    chat: Chat
    from_user: User
    date: int
    text: str = None
    caption: str = None
    photo: list[PhotoSize] = None
    entities: list = None
    edit_date: int = None
    reply_markup: InlineKeyboardMarkup = None

    async def answer(self, text: str, parse_mode: str = None, reply_markup: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove] = ReplyKeyboardMarkup()) -> 'Message':
        return await self.bot.send_message(chat_id=self.chat.id, text=text, parse_mode=parse_mode, reply_markup=reply_markup)

    async def answer_photo(self, photo: Union[InputFile, str], caption: str = None, parse_mode: Literal['HTML', 'MARKDOWN'] = None, reply_markup: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove] = ReplyKeyboardMarkup()) -> 'Message':
        return await self.bot.send_photo(chat_id=self.chat.id, photo=photo, caption=caption, parse_mode=parse_mode, reply_markup=reply_markup)

    async def delete(self):
        return await self.bot.delete_message(chat_id=self.chat.id, message_id=self.message_id)

    async def edit_text(self, text: str, reply_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(), parse_mode: str = None) -> 'Message':
        return await self.bot.edit_message_text(chat_id=self.chat.id, text=text, message_id=self.message_id, parse_mode=parse_mode, reply_markup=reply_markup)