from blazogram import Bot, Dispatcher
from blazogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio


bot = Bot(token='6091490850:AAGyqrHphgeVhF-jGBAPLp1waazyoJsDgpQ')
dp = Dispatcher()


@dp.callback_query()
async def test(callback: CallbackQuery):
    await callback.message.delete()


async def main():
    await bot.skip_updates()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
