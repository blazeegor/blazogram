from blazogram import Bot, Dispatcher, Router
from blazogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from blazogram.filters import Command, Text, StateFilter, Data
from blazogram.fsm import FSMContext
from blazogram.scheduler import BlazeScheduler
import asyncio
from my_handlers import router


async def main():
    bot = Bot(token='6091490850:AAGyqrHphgeVhF-jGBAPLp1waazyoJsDgpQ', parse_mode='HTML')
    scheduler = BlazeScheduler()
    dp = Dispatcher()
    dp.include_router(router)
    await bot.skip_updates()
    try:
        await dp.start_polling(bot, allowed_updates=['message', 'callback_query'])
    except asyncio.CancelledError:
        pass
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())