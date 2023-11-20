from ..bot.bot import Bot
from .router import Router
from ..types import Update
from ..fsm.storage.base import BaseStorage, UserKey
from ..fsm.storage.memory import MemoryStorage
from ..fsm.context import FSMContext
from ..filters import StateFilter
from ..scheduler import BlazeScheduler
from ..database import Database, MemoryDatabase
from ..middlewares.database import DatabaseMiddleware
from ..middlewares.handler import HandlerMiddlewares
from ..localization import BlazeLocale
from typing import Optional
import inspect
import asyncio


class Data:
    def __init__(self):
        self.data = {}

    def add_field(self, key: str, value) -> None:
        self.data[key] = value

    def __dict__(self) -> dict:
        return self.data


def get_data(args: list, bot: Bot, dispatcher, fsm_context: FSMContext, locale: BlazeLocale, my_data: dict) -> dict:
    data = {}

    if 'bot' in args:
        data['bot'] = bot

    if 'dp' in args:
        data['dp'] = dispatcher

    if 'state' in args:
        data['state'] = fsm_context

    if 'scheduler' in args:
        data['scheduler'] = dispatcher.scheduler

    if 'locale' in args:
        data['locale'] = locale

    data.update({key: value for key, value in my_data.items() if key in args})
    return data


class Dispatcher(Router):
    def __init__(self, scheduler: BlazeScheduler = BlazeScheduler(),
                 fsm_storage: BaseStorage = MemoryStorage(),
                 database: Optional[Database] = MemoryDatabase()):
        super().__init__()

        self.data = Data()
        self.scheduler = scheduler
        self.fsm_storage = fsm_storage
        self.database = database
        self.locale = BlazeLocale()
        self.keep_polling = True

        if self.database:
            self.register_middleware(DatabaseMiddleware(database=database))

    def include_router(self, router: Router):
        self.handlers.extend(router.handlers)

    def include_routers(self, *routers: Router):
        for router in routers:
            self.include_router(router)

    async def start_polling(self, bot: Bot, allowed_updates: list = None):
        if self.database:
            bot.connect_database(database=self.database)

        if self.locale:
            bot.connect_locale(locale=self.locale)

        task_polling = asyncio.create_task(self._polling(bot=bot, allowed_updates=allowed_updates))
        task_scheduler = asyncio.create_task(self.scheduler.start(dispatcher=self))
        await asyncio.wait([task_polling, task_scheduler])

    async def _polling(self, bot: Bot, allowed_updates: list):
        offset = None
        while self.keep_polling:
            updates = await bot.get_updates(offset=offset, allowed_updates=allowed_updates)
            if updates:
                await asyncio.wait([asyncio.create_task(self._feed_update(update=update,
                                                                          bot=bot)) for update in updates])
                offset = [update.update_id for update in updates][-1] + 1

    async def _feed_update(self, update: Update, bot: Bot):
        for handler in self.handlers:
            if handler.update == update.update:
                check = True
                event = None
                user_key = None

                if update.message:
                    event = update.message
                    user_key = UserKey(chat_id=event.chat.id, user_id=event.from_user.id)

                elif update.callback_query:
                    event = update.callback_query
                    user_key = UserKey(chat_id=event.message.chat.id, user_id=event.from_user.id)

                elif update.inline_query:
                    event = update.inline_query
                    user_key = UserKey(chat_id=event.from_user.id, user_id=event.from_user.id)

                fsm_context = FSMContext(key=user_key, storage=self.fsm_storage)

                for Filter in handler.filters:
                    argument = event if not isinstance(Filter, StateFilter) else await fsm_context.get_state()
                    if not await Filter.__check__(argument):
                        check = False

                if check:
                    args = inspect.getfullargspec(handler.func).args
                    my_data = self.data.__dict__()
                    data = get_data(args=args, bot=bot,
                                    dispatcher=self, fsm_context=fsm_context,
                                    locale=self.locale, my_data=my_data)
                    if handler.middlewares:
                        middlewares = HandlerMiddlewares(func=handler.func, args=args, data=data, update=event,
                                                         middlewares=handler.middlewares)
                        await middlewares.start()
                    else:
                        await handler.func(event, **data)
                    break

    def stop_polling(self):
        self.keep_polling = False
