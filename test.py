from blazogram import Bot, Dispatcher, BlazeLocale
from blazogram.types import Message, CallbackQuery, InlineQuery
from blazogram.filters import Command, Data
from blazogram.enums import ParseMode, Languages

import asyncio


async def start_command(message: Message, locale: BlazeLocale):
    locale.set_language(message.from_user.id, Languages.FR)
    await message.answer(text='Hello World!')


async def some_command(message: Message):
    await message.answer('Hello!')


async def main():
    bot = Bot(token='6091490850:AAGyqrHphgeVhF-jGBAPLp1waazyoJsDgpQ', parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.message.register(start_command, Command("start"))
    dp.message.register(some_command, Command('some'))

    await bot.skip_updates()
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())