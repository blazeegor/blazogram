from blazogram import Bot, Dispatcher
from blazogram.types import Message
from blazogram.filters import Command, StateFilter
from blazogram.fsm import FSMContext, State, StatesGroup
import asyncio


MyStatesGroup = StatesGroup(State(name='name'), State(name='age'))


async def start_bot(message: Message, state: FSMContext):
    await message.answer('Hello World!')
    await state.set_state(MyStatesGroup.start())
    print(await state.get_state())


async def state_handler(message: Message, state: FSMContext):
    await state.set_state(MyStatesGroup.next())
    print(await state.get_state())


async def main():
    bot = Bot(token='6091490850:AAGyqrHphgeVhF-jGBAPLp1waazyoJsDgpQ')
    dp = Dispatcher()

    dp.message.register(start_bot, Command("start"))
    dp.message.register(state_handler, StateFilter(MyStatesGroup.get_state('name')))

    await bot.skip_updates()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
