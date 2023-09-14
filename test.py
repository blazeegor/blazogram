from blazogram import Bot, Dispatcher, Router
from blazogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from blazogram.filters import Command, Text, StateFilter, Data
from blazogram.fsm import FSMContext
from blazogram.scheduler import BlazeScheduler
import asyncio
from datetime import datetime, timedelta


router = Router()


async def test_func(text):
    print(text)


@router.message(Command("start"))
async def some_func(message: Message, bot: Bot, state: FSMContext):
    ikb = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text='BUTTON', callback_data='button_data')
    ikb.add_button(button)
    await bot.send_message(chat_id=message.from_user.id, text='<b>Hello!</b>', reply_markup=ikb)


@router.callback_query(Data(data='button_data'))
async def test_data(callback: CallbackQuery, bot: Bot):
    await bot.send_message(callback.from_user.id, 'TOP!')


@router.message()
async def test_handler(message: Message, state: FSMContext):
    await message.answer('<b>Неизвестная команда!</b>')
    await state.clear()


async def main():
    bot = Bot(token='6091490850:AAGyqrHphgeVhF-jGBAPLp1waazyoJsDgpQ', parse_mode='HTML')
    scheduler = BlazeScheduler()
    dp = Dispatcher()
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