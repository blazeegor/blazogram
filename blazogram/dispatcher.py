from .bot import Bot
from .router import Router
from .types import Message, CallbackQuery, Chat, User
from .fsm.storage.base import BaseStorage, UserKey
from .fsm.storage.memory import MemoryStorage
from .fsm.context import FSMContext
from .filters import StateFilter
from .scheduler import BlazeScheduler
import inspect
import asyncio


async def feed_update(update: dict, handlers: list, bot: Bot, fsm_storage: BaseStorage, scheduler: BlazeScheduler):
    if handlers[1] in update.keys():
        for handler in handlers:
            if handler[1] == 'message':
                message = update['message']
                chat = Chat(id=message['chat']['id'], type=message['chat']['type'],
                            first_name=message['chat']['first_name'], username=message['chat']['username'])
                user = User(id=message['from']['id'], is_bot=message['from']['is_bot'],
                            first_name=message['from']['first_name'], username=message['from']['username'])
                message = Message(bot=bot, message_id=message['message_id'], text=message['text'], chat=chat, user=user)
                filters = handler[2]
                fsm_context = FSMContext(key=UserKey(chat_id=message.chat.id, user_id=message.from_user.id),
                                         storage=fsm_storage)
                check = True
                for Filter in filters:
                    argument = message if not isinstance(Filter, StateFilter) else await fsm_context.get_state()
                    if not await Filter.__check__(argument):
                        check = False
                if check is True:
                    data = dict()
                    args = inspect.getfullargspec(handler[0]).args
                    if 'bot' in args:
                        data['bot'] = bot
                    if 'state' in args:
                        data['state'] = fsm_context
                    if 'scheduler' in args:
                        data['scheduler'] = scheduler
                    await handler[0](message, **data)
                    break
            elif handler[1] == 'callback_query':
                callback_query = update['callback_query']
                user = User(id=callback_query['from']['id'], is_bot=callback_query['from']['is_bot'],
                            first_name=callback_query['from']['first_name'],
                            username=callback_query['from']['username'])
                message = Message(bot=bot, message_id=update['callback_query']['message']['message_id'],
                                  text=update['callback_query']['message']['text'],
                                  user=User(id=update['callback_query']['message']['from']['id'],
                                            is_bot=update['callback_query']['message']['from']['is_bot'],
                                            first_name=update['callback_query']['message']['from']['first_name'],
                                            username=update['callback_query']['message']['from']['username']),
                                  chat=Chat(id=update['callback_query']['message']['chat']['id'],
                                            type=update['callback_query']['message']['chat']['type'],
                                            first_name=update['callback_query']['message']['chat']['first_name'],
                                            username=update['callback_query']['message']['chat']['username']))
                callback_query = CallbackQuery(bot=bot, callback_query_id=callback_query['id'],
                                               data=callback_query['data'], message=message, user=user)
                filters = handler[2]
                fsm_context = FSMContext(
                    key=UserKey(chat_id=callback_query.message.chat.id, user_id=callback_query.from_user.id),
                    storage=fsm_storage)
                check = True
                for Filter in filters:
                    argument = callback_query if not isinstance(Filter, StateFilter) else await fsm_context.get_state()
                    if not await Filter.__check__(argument):
                        check = False
                if check is True:
                    data = dict()
                    args = inspect.getfullargspec(handler[0]).args
                    if 'bot' in args:
                        data['bot'] = bot
                    elif 'state' in args:
                        data['state'] = fsm_context
                    elif 'scheduler' in args:
                        data['scheduler'] = scheduler
                    await handler[0](callback_query, **data)
                    break


async def polling(bot: Bot, allowed_updates, self):
    while True:
        updates = await bot.get_updates(offset=self.offset, allowed_updates=allowed_updates)
        if updates:
            await asyncio.wait([asyncio.create_task(feed_update(update, self.handlers, bot, self.fsm_storage, self.scheduler)) for update in updates])
            self.offset = [update['update_id'] for update in updates][-1] + 1


class Dispatcher:
    def __init__(self, scheduler: BlazeScheduler = BlazeScheduler(), fsm_storage: BaseStorage = MemoryStorage()):
        self.scheduler = scheduler
        self.fsm_storage = fsm_storage
        self.handlers = []
        self.offset = None

    def include_router(self, router: Router):
        for handler in router.handlers:
            self.handlers.append(handler)

    def include_routers(self, *routers: Router):
        for router in routers:
            self.include_router(router)

    async def start_polling(self, bot: Bot, allowed_updates: list = None):
        task_polling = asyncio.create_task(polling(bot, allowed_updates, self))
        task_scheduler = asyncio.create_task(self.scheduler.start())
        await asyncio.wait([task_polling, task_scheduler])