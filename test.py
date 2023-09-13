from blazogram import Bot, Dispatcher, Router
from blazogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from blazogram.filters import Command, Text, StateFilter
from blazogram.fsm.context import FSMContext
from blazogram.scheduler import BlazeScheduler
import asyncio
from datetime import datetime, timedelta


router = Router()


@router.message(Command("start"))
async def some_func(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id, text='<b>Hello!</b>', reply_markup=ReplyKeyboardRemove())


@router.message()
async def test_handler(message: Message, state: FSMContext):
    await message.answer('<b>Неизвестная команда!</b>')
    await state.clear()


async def test_func(text):
    print(text)


async def main():
    bot = Bot(token='6091490850:AAGyqrHphgeVhF-jGBAPLp1waazyoJsDgpQ', parse_mode='HTML')
    scheduler = BlazeScheduler()
    scheduler.add_job(test_func, run_date=datetime.now() + timedelta(minutes=1), kwargs={'text': 'TEXT'})
    dp = Dispatcher(scheduler=scheduler)
    dp.include_routers(router)
    await bot.skip_updates()
    try:
        await dp.start_polling(bot, allowed_updates=['message', 'callback_query'])
    except asyncio.CancelledError:
        pass
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())