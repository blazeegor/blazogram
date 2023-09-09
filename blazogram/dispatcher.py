from .bot import Bot
from .router import Router
from .types import Message, CallbackQuery, Chat, User


class Dispatcher(Router):
    def include_router(self, router: Router):
        for handler in router.handlers:
            self.handlers.append(handler)

    def include_routers(self, *routers: Router):
        for router in routers:
            self.include_router(router)

    async def start_polling(self, bot: Bot):
        while True:
            updates = await bot.get_updates()
            for update in updates:
                if 'message' in update.keys():
                    for handler in self.handlers:
                        if handler[1] == 'message':
                            message = update['message']
                            chat = Chat(id=message['chat']['id'], type=message['chat']['type'], first_name=message['chat']['first_name'], username=message['chat']['username'])
                            user = User(id=message['from']['id'], is_bot=message['from']['is_bot'], first_name=message['from']['first_name'], username=message['from']['username'])
                            message = Message(bot=bot, message_id=message['message_id'], text=message['text'], chat=chat, user=user)
                            filters = handler[2]
                            check = True
                            for Filter in filters:
                               if not await Filter.__check__(message):
                                   check = False
                            if check is True:
                                await handler[0](message)
                                break
                if 'callback_query' in update.keys():
                    for handler in self.handlers:
                        if handler[1] == 'callback_query':
                            callback_query = update['callback_query']
                            user = User(id=callback_query['from']['id'], is_bot=callback_query['from']['is_bot'], first_name=callback_query['from']['first_name'], username=callback_query['from']['username'])
                            message = Message(bot=bot, message_id=update['callback_query']['message']['message_id'], text=update['callback_query']['message']['text'], user=User(id=update['callback_query']['message']['from']['id'], is_bot=update['callback_query']['message']['from']['is_bot'], first_name=update['callback_query']['message']['from']['first_name'], username=update['callback_query']['message']['from']['username']), chat=Chat(id=update['callback_query']['message']['chat']['id'], type=update['callback_query']['message']['chat']['type'], first_name=update['callback_query']['message']['chat']['first_name'], username=update['callback_query']['message']['chat']['username']))
                            callback_query = CallbackQuery(bot=bot, callback_query_id=callback_query['id'], data=callback_query['data'], message=message, user=user)
                            filters = handler[3]
                            check = True
                            for Filter in filters:
                                if not Filter.__check__(callback_query):
                                    check = False
                            if check is True:
                                await handler[0](callback_query)
                                break
            await bot.skip_updates()