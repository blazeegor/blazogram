from ..bot.bot import Bot
from .router import Router
from ..types import Message, CallbackQuery, Chat, User
from ..types.documents_types import PhotoSize
from ..fsm.storage.base import BaseStorage, UserKey
from ..fsm.storage.memory import MemoryStorage
from ..fsm.context import FSMContext
from ..filters import StateFilter
from ..scheduler import BlazeScheduler
from ..database.base import Database
from ..middlewares.database import DatabaseMiddleware

from ..middlewares.handler_middlewares import HandlerMiddlewares
import inspect
import asyncio


class Data:
    def __init__(self):
        self.data = {}

    def add_field(self, key: str, value) -> None:
        self.data[key] = value

    def __dict__(self) -> dict:
        return self.data


def get_data(args: list, bot: Bot, dispatcher, fsm_context: FSMContext, my_data: dict) -> dict:
    data = {}
    if 'bot' in args:
        data['bot'] = bot
    if 'dp' in args:
        data['dp'] = dispatcher
    if 'state' in args:
        data['state'] = fsm_context
    if 'scheduler' in args:
        data['scheduler'] = dispatcher.scheduler
    data.update({key: value for key, value in my_data.items() if key in args})
    return data


class Dispatcher(Router):
    def __init__(self, scheduler: BlazeScheduler = BlazeScheduler(), fsm_storage: BaseStorage = MemoryStorage(), database: Database = None):
        super().__init__()
        self.data = Data()
        self.scheduler = scheduler
        self.fsm_storage = fsm_storage
        self.database = database
        self.keep_polling = True

        if self.database:
            self.register_middleware(DatabaseMiddleware(database=database))

    def include_router(self, router: Router):
        self.handlers.extend([handler for handler in router.handlers])

    def include_routers(self, *routers: Router):
        for router in routers:
            self.include_router(router)

    async def start_polling(self, bot: Bot, allowed_updates: list = None):
        if self.database:
            await bot.connect_database(database=self.database)

        task_polling = asyncio.create_task(self._polling(bot=bot, allowed_updates=allowed_updates))
        task_scheduler = asyncio.create_task(self.scheduler.start(dispatcher=self))
        await asyncio.wait([task_polling, task_scheduler])

    async def _polling(self, bot: Bot, allowed_updates: list):
        offset = None
        while self.keep_polling is True:
            updates = await bot.get_updates(offset=offset, allowed_updates=allowed_updates)
            if updates:
                await asyncio.wait([asyncio.create_task(self._feed_update(update=update, handlers=self.handlers, bot=bot)) for update in updates])
                offset = [update['update_id'] for update in updates][-1] + 1

    async def _feed_update(self, update: dict, handlers: list, bot: Bot):
        for handler in handlers:
            if handler.update in update.keys():
                check = True

                if handler.update == 'message':
                    message = update['message']
                    chat = Chat(id=message['chat']['id'], type=message['chat']['type'],
                                first_name=message['chat']['first_name'], username=message['chat']['username'])
                    user = User(id=message['from']['id'], is_bot=message['from']['is_bot'],
                                first_name=message['from']['first_name'], username=message['from']['username'])

                    arguments = dict()
                    arguments['text'] = None if 'text' not in message.keys() else message['text']
                    arguments['caption'] = None if 'caption' not in message.keys() else message['caption']
                    photo = [PhotoSize(file_id=photo_size['file_id'], file_unique_id=photo_size['file_unique_id'],
                                       height=photo_size['height'], width=photo_size['width'],
                                       file_size=photo_size['file_size']) for photo_size in
                             message['photo']] if 'photo' in message.keys() else None
                    arguments['photo'] = photo

                    event = Message(bot=bot, message_id=message['message_id'], chat=chat, user=user, **arguments)
                    user_key = UserKey(chat_id=event.chat.id, user_id=event.from_user.id)

                elif handler.update == 'callback_query':
                    callback_query = update['callback_query']
                    message = callback_query['message']
                    user = User(id=callback_query['from']['id'], is_bot=callback_query['from']['is_bot'], first_name=callback_query['from']['first_name'], username=callback_query['from']['username'])

                    arguments = dict()
                    arguments['text'] = None if 'text' not in message.keys() else message['text']
                    arguments['caption'] = None if 'caption' not in message.keys() else message['caption']
                    photo = [PhotoSize(file_id=photo_size['file_id'], file_unique_id=photo_size['file_unique_id'], height=photo_size['height'], width=photo_size['width'], file_size=photo_size['file_size']) for photo_size in message['photo']] if 'photo' in message.keys() else None
                    arguments['photo'] = photo

                    message = Message(bot=bot, message_id=message['message_id'], user=User(id=message['from']['id'], is_bot=message['from']['is_bot'], first_name=message['from']['first_name'], username=message['from']['username']), chat=Chat(id=message['chat']['id'], type=message['chat']['type'], first_name=message['chat']['first_name'], username=message['chat']['username']), **arguments)
                    event = CallbackQuery(bot=bot, callback_query_id=callback_query['id'], data=callback_query['data'], message=message, user=user)
                    user_key = UserKey(chat_id=event.message.chat.id, user_id=event.from_user.id)

                else:
                    check = False
                    event = None
                    user_key = None

                filters = handler.filters
                fsm_context = FSMContext(key=user_key, storage=self.fsm_storage)
                for Filter in filters:
                    argument = event if not isinstance(Filter, StateFilter) else await fsm_context.get_state()
                    if not await Filter.__check__(argument):
                        check = False

                if check is True:
                    args = inspect.getfullargspec(handler.func).args
                    my_data = self.data.__dict__()
                    data = get_data(args=args, bot=bot, dispatcher=self, fsm_context=fsm_context, my_data=my_data)
                    if handler.middlewares:
                        middlewares = HandlerMiddlewares(func=handler.func, args=args, data=data, update=event, middlewares=handler.middlewares)
                        await middlewares.start()
                    else:
                        await handler.func(event, **data)
                    break

    def stop_polling(self):
        self.keep_polling = False