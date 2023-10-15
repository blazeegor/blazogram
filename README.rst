BLAZOGRAM - is a library for make Telegram Bots.

**Install**


.. code-block:: console


  $ pip install blazogram



**Example of use:**


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


**Developer - @Blaze Egor**