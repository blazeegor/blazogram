from blazogram import Bot, Dispatcher, Router
from blazogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from blazogram.filters import Command, Text, StateFilter
from blazogram.filters.base import BaseFilter
from blazogram.fsm.context import FSMContext
from blazogram.fsm.state import State
from blazogram.fsm.storage.memory import MemoryStorage
import asyncio


router = Router()


class MyStateGroup:
    my_state = State()


@router.message(Command("start"))
async def some_func(message: Message, bot: Bot, state: FSMContext):
    msg = await bot.send_message(chat_id=message.from_user.id, text='<b>Hello!</b>', reply_markup=ReplyKeyboardRemove())


@router.message(StateFilter(MyStateGroup.my_state))
async def test(message: Message, state: FSMContext):
    await message.answer('<b>Неизвестная команда!</b>')
    await state.clear()


async def main():
    bot = Bot(token='6091490850:AAGyqrHphgeVhF-jGBAPLp1waazyoJsDgpQ', parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(router)
    await bot.skip_updates()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())