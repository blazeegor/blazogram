from .methods import Methods
from ..types.message import Message
from ..types.reply_keyboard import ReplyKeyboardMarkup, ReplyKeyboardRemove
from ..types.inline_keyboard import InlineKeyboardMarkup
from ..types.input_file import InputFile
from ..types.user import User
from ..types.chat import Chat
from ..types.update import Update
from ..database.base import Database
from ..exceptions import TelegramBadRequest
from ..localization import BlazeLocale
from typing import Union, Optional
from ..enums import ParseMode
import asyncio


class Bot:
    def __init__(self, token: str, parse_mode: ParseMode = None):
        self.token = token
        self.parse_mode = parse_mode.name
        self.methods = Methods(bot=self)
        self.session = self.methods.session
        self.database = None
        self.locale: Optional[BlazeLocale] = None

    def connect_database(self, database: Database) -> None:
        self.database = database

    def connect_locale(self, locale: BlazeLocale):
        self.locale = locale

    async def send_all(self, text: str = None, photo: Union[str, InputFile] = None, video: Union[str, InputFile] = None, parse_mode: str = None, reply_markup: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove] = ReplyKeyboardMarkup()) -> tuple:
        number = 0
        users = await self.database.get_users()
        data = {'parse_mode': parse_mode, 'reply_markup': reply_markup}
        for user in users:
            await asyncio.sleep(0.05)
            try:
                if text:
                    await self.send_message(chat_id=user.id, text=text, **data)
                elif photo:
                    await self.send_photo(chat_id=user.id, photo=photo, **data)
                elif video:
                    await self.send_video(chat_id=user.id, video=video, **data)
            except TelegramBadRequest:
                pass
            number += 1
        return (number, len(users) - number,)

    async def send_message(self, chat_id: Union[int, str], text: str, parse_mode: str = None, reply_markup: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove] = ReplyKeyboardMarkup()) -> Message:
        return await self.methods.SendMessage(chat_id=chat_id,
                                              text=self.locale.translate(chat_id, text) if self.locale.check_user(chat_id) else text,
                                              reply_markup=reply_markup.reply_markup,
                                              parse_mode=parse_mode if parse_mode else self.parse_mode)

    async def edit_message_text(self, chat_id: Union[int, str], text: str, message_id: int, parse_mode: str, reply_markup: InlineKeyboardMarkup = InlineKeyboardMarkup()) -> Message:
        return await self.methods.EditMessageText(chat_id=chat_id, text=text, message_id=message_id, reply_markup=reply_markup.reply_markup, parse_mode=parse_mode if parse_mode else self.parse_mode)

    async def send_photo(self, chat_id: Union[int, str], photo: Union[InputFile, str], caption: str = None, parse_mode: str = None, reply_markup: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove] = InlineKeyboardMarkup()) -> Message:
        return await self.methods.SendPhoto(chat_id=chat_id, photo=photo, caption=caption, parse_mode=parse_mode if parse_mode else self.parse_mode, reply_markup=reply_markup.reply_markup)

    async def send_video(self, chat_id: Union[int, str], video: [InputFile, str], caption: str = None, parse_mode: str = None, reply_markup: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove] = InlineKeyboardMarkup()) -> Message:
        return await self.methods.SendVideo(chat_id=chat_id, video=video, caption=caption, parse_mode=parse_mode if parse_mode else self.parse_mode, reply_markup=reply_markup.reply_markup)

    async def send_chat_action(self, chat_id: Union[int, str], action: str, message_thread_id: int = None) -> bool:
        return await self.methods.SendChatAction(chat_id=chat_id, action=action, message_thread_id=message_thread_id)

    async def get_me(self) -> User:
        return await self.methods.GetMe()

    async def get_updates(self, allowed_updates: list = None, offset: int = None) -> list[Update]:
        return await self.methods.GetUpdates(offset, allowed_updates=allowed_updates)

    async def skip_updates(self):
        return await self.methods.SkipUpdates()

    async def answer_callback_query(self, callback_query_id: int, text: str = None, url: str = None, show_alert: bool = False) -> bool:
        return await self.methods.AnswerCallbackQuery(callback_query_id, text, url, show_alert)

    async def delete_message(self, chat_id: int, message_id: int):
        return await self.methods.DeleteMessage(chat_id=chat_id, message_id=message_id)

    async def get_chat(self, chat_id: int) -> Chat:
        return await self.methods.GetChat(chat_id=chat_id)