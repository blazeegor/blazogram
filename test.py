from blazogram import Bot, Dispatcher, Router
from blazogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from blazogram.filters import Command
from blazogram.filters.base import BaseFilter
import asyncio


router = Router()


class IsAdmin(BaseFilter):
    async def __check__(self, message: Message):
        return message.from_user.id == 1912790444


@router.message(IsAdmin(), Command("start"))
async def some_func(message: Message):
    msg = await message.answer('<b>Hello!</b>', reply_markup=ReplyKeyboardRemove())


@router.message()
async def test(message: Message):
    await message.answer('<b>Неизвестная команда!</b>')


async def main():
    bot = Bot(token='6091490850:AAGyqrHphgeVhF-jGBAPLp1waazyoJsDgpQ', parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(router)
    await bot.skip_updates()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())