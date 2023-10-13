from ..types import User, Chat, Message, PhotoSize, InputFile
from ..exceptions import TelegramBadRequest
from typing import Union
import aiohttp
import json


class Methods:
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    async def GetUpdates(self, offset: int | None, allowed_updates: list | None):
        response = await self.session.get(url=f'https://api.telegram.org/bot{self.bot.token}/getUpdates?offset={offset}&allowed_updates={allowed_updates}')
        data = await response.json()
        if data['ok'] is True:
            return data['result']
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
            chat = Chat(id=message['chat']['id'], type=message['chat']['type'], username=message['chat']['username'], first_name=message['chat']['first_name'])
            user = User(id=message['from']['id'], is_bot=message['from']['is_bot'], username=message['from']['username'], first_name=message['from']['first_name'], last_name=None if 'last_name' not in message['from'].keys() else message['from']['last_name'])
            return Message(bot=self.bot, message_id=message['message_id'], text=message['text'], chat=chat, user=user)
        else:
            raise TelegramBadRequest(message=data["description"])

    async def EditMessageText(self, chat_id: Union[int, str], text: str, message_id: int, parse_mode: str, reply_markup: str) -> Message:
        data = {'chat_id': f'{chat_id}', 'text': text, 'message_id': message_id, 'reply_markup': reply_markup, 'parse_mode': parse_mode}
        response = await self.session.post(url=f'https://api.telegram.org/bot{self.bot.token}/editMessageText', data=data)

        data = await response.json()
        if data['ok'] is True:
            message = data['result']
            chat = Chat(id=message['chat']['id'], type=message['chat']['type'], username=message['chat']['username'], first_name=message['chat']['first_name'])
            user = User(id=message['from']['id'], is_bot=message['from']['is_bot'], username=message['from']['username'], first_name=message['from']['first_name'], last_name=None if 'last_name' not in message['from'].keys() else message['from']['last_name'])
            return Message(bot=self.bot, message_id=message['message_id'], text=message['text'], chat=chat, user=user)
        else:
            raise TelegramBadRequest(message=data["description"])

    async def SendPhoto(self, chat_id: Union[int, str], photo: Union[InputFile, str], caption: str, parse_mode: str, reply_markup: str) -> Message:
        data = {'chat_id': f'{chat_id}', 'reply_markup': reply_markup, 'parse_mode': parse_mode}

        if caption:
            data['caption'] = caption

        data['photo'] = photo if isinstance(photo, str) else photo.file
        response = await self.session.post(url=f'https://api.telegram.org/bot{self.bot.token}/sendPhoto', data=data)

        data = await response.json()
        if data['ok'] is True:
            message = data['result']
            chat = Chat(id=message['chat']['id'], type=message['chat']['type'], username=message['chat']['username'], first_name=message['chat']['first_name'])
            user = User(id=message['from']['id'], is_bot=message['from']['is_bot'], username=message['from']['username'], first_name=message['from']['first_name'], last_name=None if 'last_name' not in message['from'].keys() else message['from']['last_name'])
            photo = [PhotoSize(file_id=photo_size['file_id'], file_unique_id=photo_size['file_unique_id'], height=photo_size['height'], width=photo_size['width'], file_size=photo_size['file_size']) for photo_size in message['photo']]
            caption = None if 'caption' not in message.keys() else message['caption']
            return Message(bot=self.bot, message_id=message['message_id'], caption=caption, photo=photo, chat=chat, user=user)
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

    async def AnswerCallbackQuery(self, callback_query_id: int, text: str, show_alert: bool):
        response = await self.session.get(url=f'https://api.telegram.org/bot{self.bot.token}/answerCallbackQuery?callback_query_id={callback_query_id}&text={text}&show_alert={show_alert}')
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