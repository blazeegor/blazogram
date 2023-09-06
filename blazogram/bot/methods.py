from blazogram.types import User, Chat
import aiohttp


class Methods:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token

    async def SendMessage(self, chat_id: int, text: str, reply_markup: str):
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=f'https://api.telegram.org/bot{self.bot_token}/sendMessage?chat_id={chat_id}&text={text}&reply_markup={reply_markup}')
            data = await response.json()
            if data['ok'] is True:
                result = data['result']
                return result
            else:
                raise ValueError(f'Error code: {data["error_code"]}. {data["description"]}')

    async def GetMe(self):
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=f'https://api.telegram.org/bot{self.bot_token}/getMe')
            data = await response.json()
            if data['ok'] is True:
                result = data['result']
                return User(id=result['id'], first_name=result['first_name'], username=result['username'])
            else:
                raise ValueError(f'Error code: {data["error_code"]}. {data["description"]}')

    async def GetChat(self, chat_id: int):
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=f'https://api.telegram.org/bot{self.bot_token}/getChat?chat_id={chat_id}')
            data = await response.json()
            if data['ok'] is True:
                result = data['result']
                return Chat(id=result['id'], first_name=result['first_name'], username=result['username'])
            else:
                raise ValueError(data["description"])

    async def GetUpdates(self):
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=f'https://api.telegram.org/bot{self.bot_token}/getUpdates')
            data = await response.json()
            if data['ok'] is True:
                return data['result']
            else:
                raise ValueError(f'Error code: {data["error_code"]}. {data["description"]}')

    async def SkipUpdates(self):
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=f'https://api.telegram.org/bot{self.bot_token}/deleteWebhook?drop_pending_updates=True')
            data = await response.json()
            if data['ok'] is False:
                raise ValueError(f'Error code: {data["error_code"]}. {data["description"]}')

    async def AnswerCallbackQuery(self, callback_query_id: int, text: str, show_alert: bool):
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=f'https://api.telegram.org/bot{self.bot_token}/answerCallbackQuery?callback_query_id={callback_query_id}&text={text}&show_alert={show_alert}')
            data = await response.json()
            if data['ok'] is False:
                raise ValueError(data["description"])
            return True

    async def DeleteMessage(self, chat_id: int, message_id: int):
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=f'https://api.telegram.org/bot{self.bot_token}/deleteMessage?chat_id={chat_id}&message_id={message_id}')
            data = await response.json()
            if data['ok'] is False:
                raise ValueError(data["description"])
            return True