from ..types import User, Chat, Message, CallbackQuery, PhotoSize, Video, InputFile, ChatPhoto, Update, InlineKeyboardMarkup, InlineKeyboardButton
from ..exceptions import TelegramBadRequest
from typing import Union
import aiohttp


class Methods:
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    async def GetUpdates(self, offset: int | None, allowed_updates: list | None) -> list[Update]:
        response = await self.session.get(url=f'https://api.telegram.org/bot{self.bot.token}/getUpdates?offset={offset}&allowed_updates={allowed_updates}')
        data = await response.json()
        if data['ok'] is True:
            updates = []

            for update in data['result']:
                if 'message' in update.keys():
                    message = update['message']

                    message['chat'] = Chat(**message['chat'])
                    message['from_user'] = User(**message['from'])
                    message['photo'] = [PhotoSize(**photo_size) for photo_size in message['photo']] if 'photo' in message.keys() else None
                    message['reply_markup'] = InlineKeyboardMarkup(inline_keyboard=[InlineKeyboardButton(**button[0]) for button in message['reply_markup']['inline_keyboard']]) if 'reply_markup' in message.keys() else None

                    message.pop('from')

                    update['message'] = Message(bot=self.bot, **message)
                    update['update'] = 'message'

                elif 'callback_query' in update.keys():
                    callback_query = update['callback_query']
                    message = callback_query['message']

                    callback_query['from_user'] = User(**callback_query['from'])
                    message['chat'] = Chat(**message['chat'])
                    message['from_user'] = User(**message['from'])
                    message['photo'] = [PhotoSize(**photo_size) for photo_size in message['photo']] if 'photo' in message.keys() else None
                    message['reply_markup'] = InlineKeyboardMarkup(inline_keyboard=[InlineKeyboardButton(**button[0]) for button in message['reply_markup']['inline_keyboard']]) if 'reply_markup' in message.keys() else None

                    callback_query.pop('from')
                    message.pop('from')

                    callback_query['message'] = Message(bot=self.bot, **message)

                    update['callback_query'] = CallbackQuery(bot=self.bot, **callback_query)
                    update['update'] = 'callback_query'

                updates.append(Update(**update))

            return updates
        else:
            raise TelegramBadRequest(message=data["description"])

    async def SkipUpdates(self):
        response = await self.session.get(url=f'https://api.telegram.org/bot{self.bot.token}/deleteWebhook?drop_pending_updates=True')
        data = await response.json()
        if data['ok'] is True:
            return True
        else:
           raise TelegramBadRequest(message=data["description"])

    async def SendMessage(self, chat_id: Union[int, str], text: str, reply_markup: str, parse_mode: str) -> Message:
        data = {'chat_id': f'{chat_id}', 'text': text, 'reply_markup': reply_markup, 'parse_mode': parse_mode}
        response = await self.session.get(url=f'https://api.telegram.org/bot{self.bot.token}/sendMessage', data=data)

        data = await response.json()
        if data['ok'] is True:
            message = data['result']
            message['chat']['photo'] = None if 'photo' not in message['chat'].keys() else ChatPhoto(**message['chat']['photo'])
            message['chat'] = Chat(**message['chat'])
            message['from_user'] = User(**message['from'])
            message.pop('from')
            return Message(bot=self.bot, **message)
        else:
            raise TelegramBadRequest(message=data["description"])

    async def EditMessageText(self, chat_id: Union[int, str], text: str, message_id: int, parse_mode: str, reply_markup: str) -> Message:
        data = {'chat_id': f'{chat_id}', 'text': text, 'message_id': message_id, 'reply_markup': reply_markup, 'parse_mode': parse_mode}

        response = await self.session.post(url=f'https://api.telegram.org/bot{self.bot.token}/editMessageText', data=data)

        data = await response.json()
        if data['ok'] is True:
            message = data['result']
            message['chat'] = Chat(**message['chat'])
            message['from_user'] = User(**message['from'])
            message.pop('from')
            return Message(bot=self.bot, **message)
        else:
            raise TelegramBadRequest(message=data["description"])

    async def SendPhoto(self, chat_id: Union[int, str], photo: Union[InputFile, str], caption: str, parse_mode: str, reply_markup: str) -> Message:
        data = {'chat_id': f'{chat_id}', 'photo': photo if isinstance(photo, str) else photo.file, 'reply_markup': reply_markup, 'parse_mode': parse_mode}

        if caption:
            data['caption'] = caption

        response = await self.session.post(url=f'https://api.telegram.org/bot{self.bot.token}/sendPhoto', data=data)

        data = await response.json()
        if data['ok'] is True:
            message = data['result']
            message['chat'] = Chat(**message['chat'])
            message['from_user'] = User(**message['from'])
            message['photo'] = [PhotoSize(**photo_size) for photo_size in message['photo']]

            message.pop('from')

            return Message(bot=self.bot, **message)
        else:
            raise TelegramBadRequest(message=data["description"])

    async def SendVideo(self, chat_id: Union[int, str], video: Union[InputFile, str], caption: str, parse_mode: str, reply_markup: str) -> Message:
        data = {'chat_id': f'{chat_id}', 'reply_markup': reply_markup, 'parse_mode': parse_mode, 'video': video if isinstance(video, str) else video.file}

        if caption:
            data['caption'] = caption

        response = await self.session.post(url=f'https://api.telegram.org/bot{self.bot.token}/sendVideo', data=data)

        data = await response.json()
        if data['ok'] is True:
            message = data['result']
            message['chat'] = Chat(**message['chat'])
            message['from_user'] = User(**message['from'])
            message['video'] = Video(**message['video'])

            message.pop('from')

            return Message(bot=self.bot, **message)
        else:
            raise TelegramBadRequest(message=data["description"])

    async def SendChatAction(self, chat_id: Union[int, str], action: str, message_thread_id: int) -> bool:
        data = {'chat_id': chat_id, 'action': action}

        if message_thread_id:
            data['message_thread_id'] = message_thread_id

        response = await self.session.get(url=f'https://api.telegram.org/bot{self.bot.token}/sendChatAction', data=data)
        data = await response.json()
        if data['ok'] is True:
            return True
        else:
            raise TelegramBadRequest(message=data["description"])

    async def GetMe(self) -> User:
        response = await self.session.get(url=f'https://api.telegram.org/bot{self.bot.token}/getMe')
        data = await response.json()
        if data['ok'] is True:
            result = data['result']
            return User(id=result['id'], is_bot=result['is_bot'], first_name=result['first_name'], username=result['username'])
        else:
            raise TelegramBadRequest(message=data["description"])

    async def GetChat(self, chat_id: int) -> Chat:
        response = await self.session.get(url=f'https://api.telegram.org/bot{self.bot.token}/getChat?chat_id={chat_id}')
        data = await response.json()
        if data['ok'] is True:
            result = data['result']
            chat = Chat(id=result['id'], type=result['type'], first_name=result['first_name'], username=result['username'])
            return chat
        else:
            raise TelegramBadRequest(message=data["description"])

    async def AnswerCallbackQuery(self, callback_query_id: int, text: str, url: str, cache_time: int, show_alert: bool) -> bool:
        data = {'callback_query_id': callback_query_id, 'show_alert': show_alert}
        if text:
            data['text'] = text
        if url:
            data['url'] = url

        response = await self.session.post(url=f'https://api.telegram.org/bot{self.bot.token}/answerCallbackQuery', data=data)

        data = await response.json()
        if data['ok'] is True:
            return True
        else:
            raise TelegramBadRequest(message=data["description"])

    async def DeleteMessage(self, chat_id: int, message_id: int):
        response = await self.session.get(url=f'https://api.telegram.org/bot{self.bot.token}/deleteMessage?chat_id={chat_id}&message_id={message_id}')
        data = await response.json()
        if data['ok'] is True:
            return True
        else:
            raise TelegramBadRequest(message=data["description"])