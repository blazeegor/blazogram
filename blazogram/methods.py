from .types import User, Chat, Message
from .types.objects import PhotoSize, InputFile
from .exceptions import TelegramBadRequest
from typing import Union
import aiohttp


class Methods:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.session = aiohttp.ClientSession()

    async def GetUpdates(self, offset: int | None, allowed_updates: list | None):
        response = await self.session.get(url=f'https://api.telegram.org/bot{self.bot_token}/getUpdates?offset={offset}&allowed_updates={allowed_updates}')
        data = await response.json()
        if data['ok'] is True:
            return data['result']
        else:
            raise TelegramBadRequest(message=data["description"])

    async def SkipUpdates(self):
        response = await self.session.get(url=f'https://api.telegram.org/bot{self.bot_token}/deleteWebhook?drop_pending_updates=True')
        data = await response.json()
        if data['ok'] is True:
            return True
        else:
           raise TelegramBadRequest(message=data["description"])

    async def SendMessage(self, chat_id: int, text: str, reply_markup: str, parse_mode: str) -> Message:
        from .bot import Bot
        response = await self.session.get(url=f'https://api.telegram.org/bot{self.bot_token}/sendMessage?chat_id={chat_id}&text={text}&reply_markup={reply_markup}&parse_mode={parse_mode}')
        data = await response.json()
        if data['ok'] is True:
            message = data['result']
            chat = Chat(id=message['chat']['id'], type=message['chat']['type'], username=message['chat']['username'], first_name=message['chat']['first_name'])
            user = User(id=message['from']['id'], is_bot=message['from']['is_bot'], username=message['from']['username'], first_name=message['from']['first_name'])
            return Message(bot=Bot(token=self.bot_token), message_id=message['message_id'], text=message['text'], chat=chat, user=user)
        else:
            raise TelegramBadRequest(message=data["description"])

    async def SendPhoto(self, chat_id: int, photo: Union[InputFile, str], caption: str, parse_mode: str, reply_markup: str) -> Message:
        from .bot import Bot
        params = f'chat_id={chat_id}&reply_markup={reply_markup}&parse_mode={parse_mode}'
        if caption:
            params += f'&caption={caption}'
        data = {'photo': photo} if isinstance(photo, str) else photo.data
        response = await self.session.post(url=f'https://api.telegram.org/bot{self.bot_token}/sendPhoto?{params}', data=data)
        if isinstance(photo, InputFile):
            photo.file.close()
        data = await response.json()
        if data['ok'] is True:
            message = data['result']
            chat = Chat(id=message['chat']['id'], type=message['chat']['type'], username=message['chat']['username'], first_name=message['chat']['first_name'])
            user = User(id=message['from']['id'], is_bot=message['from']['is_bot'], username=message['from']['username'], first_name=message['from']['first_name'])
            photo = [PhotoSize(file_id=photo_size['file_id'], file_unique_id=photo_size['file_unique_id'], height=photo_size['height'], width=photo_size['width'], file_size=photo_size['file_size']) for photo_size in message['photo']]
            caption = None if 'caption' not in message.keys() else message['caption']
            return Message(bot=Bot(token=self.bot_token), message_id=message['message_id'], caption=caption, photo=photo, chat=chat, user=user)
        else:
            raise TelegramBadRequest(message=data["description"])

    async def GetMe(self) -> User:
        response = await self.session.get(url=f'https://api.telegram.org/bot{self.bot_token}/getMe')
        data = await response.json()
        if data['ok'] is True:
            result = data['result']
            return User(id=result['id'], is_bot=result['is_bot'], first_name=result['first_name'], username=result['username'])
        else:
            raise TelegramBadRequest(message=data["description"])

    async def GetChat(self, chat_id: int) -> Chat:
        response = await self.session.get(url=f'https://api.telegram.org/bot{self.bot_token}/getChat?chat_id={chat_id}')
        data = await response.json()
        if data['ok'] is True:
            result = data['result']
            chat = Chat(id=result['id'], type=result['type'], first_name=result['first_name'], username=result['username'])
            return chat
        else:
            raise TelegramBadRequest(message=data["description"])

    async def AnswerCallbackQuery(self, callback_query_id: int, text: str, show_alert: bool):
        response = await self.session.get(url=f'https://api.telegram.org/bot{self.bot_token}/answerCallbackQuery?callback_query_id={callback_query_id}&text={text}&show_alert={show_alert}')
        data = await response.json()
        if data['ok'] is True:
            return True
        else:
            raise TelegramBadRequest(message=data["description"])

    async def DeleteMessage(self, chat_id: int, message_id: int):
        response = await self.session.get(url=f'https://api.telegram.org/bot{self.bot_token}/deleteMessage?chat_id={chat_id}&message_id={message_id}')
        data = await response.json()
        if data['ok'] is True:
            return True
        else:
            raise TelegramBadRequest(message=data["description"])