from ..types.user import User
from ..types.chat import Chat
from ..types.message import Message
from ..types.callback_query import CallbackQuery
from ..types.photo import PhotoSize, ChatPhoto
from ..types.video import Video
from ..types.input_file import InputFile
from ..types.update import Update
from ..types.inline_keyboard import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboard,
    InlineKeyboardLine,
)
from ..types.inline_query import InlineQuery
from ..types.location import Location
from ..exceptions import TelegramBadRequest
from typing import Union, Optional
import aiohttp


class Methods:
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    async def GetUpdates(
        self, offset: Optional[int], allowed_updates: Optional[list]
    ) -> list[Update]:
        data = {"offset": offset, "allowed_updates": allowed_updates}
        response = await self.session.get(
            url=f"https://api.telegram.org/bot{self.bot.token}/getUpdates", data=data
        )

        data = await response.json()

        if data["ok"] is True:
            updates = []

            for update in data["result"]:
                if "message" in update:
                    message = update["message"]

                    message["chat"] = Chat(**message["chat"])
                    message["from_user"] = User(**message["from"])

                    if "photo" in message:
                        message["photo"] = [
                            PhotoSize(**photo_size) for photo_size in message["photo"]
                        ]

                    if "reply_markup" in message:
                        inline_keyboard_list = message["reply_markup"][
                            "inline-keyboard"
                        ]

                        inline_keyboard = InlineKeyboard()
                        for line_list in inline_keyboard_list:
                            line = InlineKeyboardLine()
                            for button_dict in line_list:
                                button = InlineKeyboardButton(**button_dict)
                                line.add_buttons(button)
                            inline_keyboard.add_lines(line)

                        message["reply_markup"] = InlineKeyboardMarkup(
                            inline_keyboard=inline_keyboard
                        )

                    message.pop("from")

                    update["message"] = Message(bot=self.bot, **message)
                    update["update"] = "message"

                elif "callback_query" in update:
                    callback_query = update["callback_query"]
                    message = callback_query["message"]

                    callback_query["from_user"] = User(**callback_query["from"])
                    message["chat"] = Chat(**message["chat"])
                    message["from_user"] = User(**message["from"])
                    message["photo"] = (
                        [PhotoSize(**photo_size) for photo_size in message["photo"]]
                        if "photo" in message.keys()
                        else None
                    )

                    if "reply_markup" in message:
                        inline_keyboard_list = message["reply_markup"][
                            "inline-keyboard"
                        ]

                        inline_keyboard = InlineKeyboard()
                        for line_list in inline_keyboard_list:
                            line = InlineKeyboardLine()
                            for button_dict in line_list:
                                button = InlineKeyboardButton(**button_dict)
                                line.add_buttons(button)
                            inline_keyboard.add_lines(line)

                        message["reply_markup"] = InlineKeyboardMarkup(
                            inline_keyboard=inline_keyboard
                        )

                    callback_query.pop("from")
                    message.pop("from")

                    callback_query["message"] = Message(bot=self.bot, **message)

                    update["callback_query"] = CallbackQuery(
                        bot=self.bot, **callback_query
                    )
                    update["update"] = "callback_query"

                elif "inline_query" in update:
                    inline_query = update["inline_query"]
                    from_user = inline_query["from"]

                    inline_query["from_user"] = User(**from_user)

                    if "location" in inline_query:
                        location = inline_query["location"]
                        inline_query["location"] = Location(**location)

                    inline_query.pop("from")

                    update["inline_query"] = InlineQuery(**inline_query)
                    update["update"] = "inline_query"

                updates.append(Update(**update))

            return updates
        else:
            raise TelegramBadRequest(message=data["description"])

    async def SkipUpdates(self):
        response = await self.session.get(
            url=f"https://api.telegram.org/bot{self.bot.token}/deleteWebhook?drop_pending_updates=True"
        )
        data = await response.json()
        if data["ok"] is True:
            return True
        raise TelegramBadRequest(message=data["description"])

    async def SendMessage(
        self, chat_id: Union[int, str], text: str, reply_markup: str, parse_mode: str
    ) -> Message:
        data = {
            "chat_id": f"{chat_id}",
            "text": text,
            "reply_markup": reply_markup,
            "parse_mode": parse_mode,
        }
        response = await self.session.get(
            url=f"https://api.telegram.org/bot{self.bot.token}/sendMessage", data=data
        )

        data = await response.json()
        if data["ok"] is True:
            message = data["result"]
            chat = message["chat"]
            from_user = message["from"]

            if "photo" in chat:
                chat["photo"] = ChatPhoto(**chat["photo"])

            message["chat"] = Chat(**chat)
            message["from_user"] = User(**from_user)

            if "reply_markup" in message:
                inline_keyboard_list = message["reply_markup"]["inline-keyboard"]

                inline_keyboard = InlineKeyboard()
                for line_list in inline_keyboard_list:
                    line = InlineKeyboardLine()
                    for button_dict in line_list:
                        button = InlineKeyboardButton(**button_dict)
                        line.add_buttons(button)
                    inline_keyboard.add_lines(line)

                message["reply_markup"] = InlineKeyboardMarkup(
                    inline_keyboard=inline_keyboard
                )

            message.pop("from")

            return Message(bot=self.bot, **message)
        else:
            raise TelegramBadRequest(message=data["description"])

    async def EditMessageText(
        self,
        chat_id: Union[int, str],
        text: str,
        message_id: int,
        parse_mode: str,
        reply_markup: str,
    ) -> Message:
        data = {
            "chat_id": f"{chat_id}",
            "text": text,
            "message_id": message_id,
            "reply_markup": reply_markup,
            "parse_mode": parse_mode,
        }
        response = await self.session.post(
            url=f"https://api.telegram.org/bot{self.bot.token}/editMessageText",
            data=data,
        )

        data = await response.json()
        if data["ok"] is True:
            message = data["result"]
            chat = message["chat"]
            from_user = message["from"]

            message["chat"] = Chat(**chat)
            message["from_user"] = User(**from_user)

            if "reply_markup" in message:
                inline_keyboard_list = message["reply_markup"]["inline-keyboard"]

                inline_keyboard = InlineKeyboard()
                for line_list in inline_keyboard_list:
                    line = InlineKeyboardLine()
                    for button_dict in line_list:
                        button = InlineKeyboardButton(**button_dict)
                        line.add_buttons(button)
                    inline_keyboard.add_lines(line)

                message["reply_markup"] = InlineKeyboardMarkup(
                    inline_keyboard=inline_keyboard
                )

            message.pop("from")

            return Message(bot=self.bot, **message)
        else:
            raise TelegramBadRequest(message=data["description"])

    async def SendPhoto(
        self,
        chat_id: Union[int, str],
        photo: Union[InputFile, str],
        caption: str,
        parse_mode: str,
        reply_markup: str,
    ) -> Message:
        data = {
            "chat_id": f"{chat_id}",
            "photo": photo if isinstance(photo, str) else photo.file,
            "reply_markup": reply_markup,
            "parse_mode": parse_mode,
        }

        if caption:
            data["caption"] = caption

        response = await self.session.post(
            url=f"https://api.telegram.org/bot{self.bot.token}/sendPhoto", data=data
        )

        data = await response.json()
        if data["ok"] is True:
            message = data["result"]
            message["chat"] = Chat(**message["chat"])
            message["from_user"] = User(**message["from"])
            message["photo"] = [
                PhotoSize(**photo_size) for photo_size in message["photo"]
            ]

            message.pop("from")

            return Message(bot=self.bot, **message)
        else:
            raise TelegramBadRequest(message=data["description"])

    async def SendVideo(
        self,
        chat_id: Union[int, str],
        video: Union[InputFile, str],
        caption: str,
        parse_mode: str,
        reply_markup: str,
    ) -> Message:
        data = {
            "chat_id": f"{chat_id}",
            "reply_markup": reply_markup,
            "parse_mode": parse_mode,
            "video": video if isinstance(video, str) else video.file,
        }

        if caption:
            data["caption"] = caption

        response = await self.session.post(
            url=f"https://api.telegram.org/bot{self.bot.token}/sendVideo", data=data
        )

        data = await response.json()
        if data["ok"] is True:
            message = data["result"]

            message["chat"] = Chat(**message["chat"])
            message["from_user"] = User(**message["from"])
            message["video"] = Video(**message["video"])

            message.pop("from")

            return Message(bot=self.bot, **message)
        else:
            raise TelegramBadRequest(message=data["description"])

    async def SendChatAction(
        self, chat_id: Union[int, str], action: str, message_thread_id: int
    ) -> bool:
        data = {"chat_id": chat_id, "action": action}

        if message_thread_id:
            data["message_thread_id"] = message_thread_id

        response = await self.session.get(
            url=f"https://api.telegram.org/bot{self.bot.token}/sendChatAction",
            data=data,
        )

        data = await response.json()
        if data["ok"] is True:
            return True
        else:
            raise TelegramBadRequest(message=data["description"])

    async def GetMe(self) -> User:
        response = await self.session.get(
            url=f"https://api.telegram.org/bot{self.bot.token}/getMe"
        )
        data = await response.json()
        if data["ok"] is True:
            result = data["result"]
            return User(**result)
        else:
            raise TelegramBadRequest(message=data["description"])

    async def GetChat(self, chat_id: int) -> Chat:
        response = await self.session.get(
            url=f"https://api.telegram.org/bot{self.bot.token}/getChat?chat_id={chat_id}"
        )

        data = await response.json()
        if data["ok"] is True:
            result = data["result"]
            chat = Chat(**result)
            return chat
        else:
            raise TelegramBadRequest(message=data["description"])

    async def AnswerCallbackQuery(
        self, callback_query_id: int, text: str, url: str, show_alert: bool
    ) -> bool:
        data = {"callback_query_id": callback_query_id, "show_alert": show_alert}

        if text:
            data["text"] = text

        if url:
            data["url"] = url

        response = await self.session.post(
            url=f"https://api.telegram.org/bot{self.bot.token}/answerCallbackQuery",
            data=data,
        )

        data = await response.json()
        if data["ok"] is True:
            return True
        else:
            raise TelegramBadRequest(message=data["description"])

    async def DeleteMessage(self, chat_id: int, message_id: int):
        data = {"chat_id": chat_id, "message_id": message_id}
        response = await self.session.get(
            url=f"https://api.telegram.org/bot{self.bot.token}/deleteMessage", data=data
        )

        data = await response.json()
        if data["ok"] is True:
            return True
        else:
            raise TelegramBadRequest(message=data["description"])
