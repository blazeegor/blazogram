from .bot.bot import Bot
from .types import Message, CallbackQuery, Chat, User


class Dispatcher:
    def __init__(self):
        self.handlers = []

    def message(self, text: str):
        def wrapper(func):
            self.handlers.append((func, 'message', text,))
        return wrapper

    def callback_query(self, data: str):
        def wrapper(func):
            self.handlers.append((func, 'callback_query', data,))
        return wrapper

    async def start_polling(self, bot: Bot):
        while True:
            updates = await bot.get_updates()
            for update in updates:
                if 'message' in update.keys():
                    for handler in self.handlers:
                        if handler[1] == 'message' and update['message']['text'] == handler[2]:
                            message = Message(bot=bot, message_id=update['message']['message_id'], text=update['message']['text'], chat=Chat(id=update['message']['chat']['id'], first_name=update['message']['chat']['first_name'], username=update['message']['chat']['username']), user=User(id=update['message']['from']['id'], first_name=update['message']['from']['first_name'], username=update['message']['from']['username']))
                            await handler[0](message)
                if 'callback_query' in update.keys():
                    for handler in self.handlers:
                        if handler[1] == 'callback_query' and update['callback_query']['data'] == handler[2]:
                            callback_query = CallbackQuery(bot=bot, callback_query_id=update['callback_query']['id'], data=update['callback_query']['data'], message=Message(bot=bot, message_id=update['callback_query']['message']['message_id'], text=update['callback_query']['message']['text'], user=User(id=update['callback_query']['message']['from']['id'], first_name=update['callback_query']['message']['from']['first_name'], username=update['callback_query']['message']['from']['username']), chat=Chat(id=update['callback_query']['message']['chat']['id'], first_name=update['callback_query']['message']['chat']['first_name'], username=update['callback_query']['message']['chat']['username'])), user=User(id=update['callback_query']['from']['id'], first_name=update['callback_query']['from']['first_name'], username=update['callback_query']['from']['username']))
                            await handler[0](callback_query)
            await bot.skip_updates()