from blazogram.bot.bot import Bot
from blazogram.dispatcher.router import Router
from blazogram.types import Message, CallbackQuery, Chat, User
from blazogram.types.objects import PhotoSize
from blazogram.fsm.storage.base import BaseStorage, UserKey
from blazogram.fsm.storage.memory import MemoryStorage
from blazogram.fsm.context import FSMContext
from blazogram.filters import StateFilter
from blazogram.scheduler import BlazeScheduler
import inspect
import asyncio


def get_data(args: list, bot: Bot, fsm_context: FSMContext, scheduler: BlazeScheduler) -> dict:
    data = dict()
    if 'bot' in args:
        data['bot'] = bot
    if 'state' in args:
        data['state'] = fsm_context
    if 'scheduler' in args:
        data['scheduler'] = scheduler
    return data


async def feed_update(update: dict, handlers: list, bot: Bot, fsm_storage: BaseStorage, scheduler: BlazeScheduler):
    for handler in handlers:
        if handler[1] in update.keys():
            if handler[1] == 'message':
                message = update['message']
                chat = Chat(id=message['chat']['id'], type=message['chat']['type'], first_name=message['chat']['first_name'], username=message['chat']['username'])
                user = User(id=message['from']['id'], is_bot=message['from']['is_bot'], first_name=message['from']['first_name'], username=message['from']['username'])

                arguments = dict()
                arguments['text'] = None if 'text' not in message.keys() else message['text']
                arguments['caption'] = None if 'caption' not in message.keys() else message['caption']
                photo = [PhotoSize(file_id=photo_size['file_id'], file_unique_id=photo_size['file_unique_id'], height=photo_size['height'], width=photo_size['width'], file_size=photo_size['file_size']) for photo_size in message['photo']] if 'photo' in message.keys() else None
                arguments['photo'] = photo

                message = Message(bot=bot, message_id=message['message_id'], chat=chat, user=user, **arguments)
                filters = handler[2]
                fsm_context = FSMContext(key=UserKey(chat_id=message.chat.id, user_id=message.from_user.id), storage=fsm_storage)
                check = True
                for Filter in filters:
                    argument = message if not isinstance(Filter, StateFilter) else await fsm_context.get_state()
                    if not await Filter.__check__(argument):
                        check = False
                if check is True:
                    args = inspect.getfullargspec(handler[0]).args
                    data = get_data(args, bot=bot, fsm_context=fsm_context, scheduler=scheduler)
                    if len(handler) == 3:
                        await handler[0](message, **data)
                    else:
                        await handler[3](handler=handler[0], update=message, data=data)
                    break
            elif handler[1] == 'callback_query':
                callback_query = update['callback_query']
                message = callback_query['message']
                user = User(id=callback_query['from']['id'], is_bot=callback_query['from']['is_bot'], first_name=callback_query['from']['first_name'], username=callback_query['from']['username'])

                arguments = dict()
                arguments['text'] = None if 'text' not in message.keys() else message['text']
                arguments['caption'] = None if 'caption' not in message.keys() else message['caption']
                photo = [PhotoSize(file_id=photo_size['file_id'], file_unique_id=photo_size['file_unique_id'], height=photo_size['height'], width=photo_size['width'], file_size=photo_size['file_size']) for photo_size in message['photo']] if 'photo' in message.keys() else None
                arguments['photo'] = photo

                message = Message(bot=bot, message_id=message['message_id'], user=User(id=message['from']['id'], is_bot=message['from']['is_bot'], first_name=message['from']['first_name'], username=message['from']['username']), chat=Chat(id=message['chat']['id'], type=message['chat']['type'], first_name=message['chat']['first_name'],  username=message['chat']['username']), **arguments)
                callback_query = CallbackQuery(bot=bot, callback_query_id=callback_query['id'], data=callback_query['data'], message=message, user=user)
                filters = handler[2]
                fsm_context = FSMContext(key=UserKey(chat_id=callback_query.message.chat.id, user_id=callback_query.from_user.id), storage=fsm_storage)
                check = True
                for Filter in filters:
                    argument = callback_query if not isinstance(Filter, StateFilter) else await fsm_context.get_state()
                    if not await Filter.__check__(argument):
                        check = False
                if check is True:
                    args = inspect.getfullargspec(handler[0]).args
                    data = get_data(args, bot=bot, fsm_context=fsm_context, scheduler=scheduler)
                    if len(handler) == 3:
                        await handler[0](callback_query, **data)
                    else:
                        await handler[3](handler=handler[0], update=message, data=data)
                    break


async def polling(bot: Bot, allowed_updates, self):
    while True:
        updates = await bot.get_updates(offset=self.offset, allowed_updates=allowed_updates)
        if updates:
            await asyncio.wait([asyncio.create_task(feed_update(update, self.handlers, bot, self.fsm_storage, self.scheduler)) for update in updates])
            self.offset = [update['update_id'] for update in updates][-1] + 1


class Dispatcher(Router):
    def __init__(self, scheduler: BlazeScheduler = BlazeScheduler(), fsm_storage: BaseStorage = MemoryStorage()):
        super().__init__()
        self.scheduler = scheduler
        self.fsm_storage = fsm_storage
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