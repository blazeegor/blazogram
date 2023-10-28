===================================
BLAZOGRAM - A Library for Telegram Bots
===================================

Install
=======

.. code-block:: console

    $ pip install blazogram

Example Usage
=============

.. code-block:: python

    from blazogram import Bot, Dispatcher
    from blazogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
    from blazogram.filters import Command, Data
    from blazogram.enums import ParseMode
    import asyncio


    async def start_command(message: Message):
        kb = ReplyKeyboardMarkup()
        button = KeyboardButton(text='BUTTON')
        kb.add_button(button)
        await message.answer(text='Hello World!', reply_markup=kb)


    async def some_func(callback: CallbackQuery):
        await callback.answer(text='Hello World!', show_alert=True)


    async def main():
        bot = Bot(token='YOUR-BOT-TOKEN', parse_mode=ParseMode.HTML)
        dp = Dispatcher()
        dp.message.register(start_command, Command("start"))
        dp.callback_query.register(some_func, Data("BUTTON_DATA"))
        await bot.skip_updates()
        try:
            await dp.start_polling(bot)
        finally:
            await bot.session.close()


    if __name__ == '__main__':
        asyncio.run(main())

Localization
============

.. code-block:: python

    from blazogram import BlazeLocale
    ...

    async def hello_handler(message: Message, i18n):
        await message.answer(i18n.format_value("hello"))

    async def main():
        bot = Bot(...)

        locales = Path(__file__).parent / "locales"
        i18n = BlazeLocale(locales)

        dp = Dispatcher()
        dp["i18n"] = i18n.get_locale("ru")

        dp.message.register(hello_handler, Command("hello")
        await dp.start_polling(bot)

**Developer: @Blaze Egor**
