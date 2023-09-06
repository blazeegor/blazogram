BLAZOGRAM - is a library for make Telegram Bots.

**Install**


.. code-block:: console
  $ pip install blazogram


**Example of use:**


.. code-block:: python
  from blazogram import Bot, Dispatcher
  from blazogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
  import asyncio


  bot = Bot(token='YOUR-BOT-TOKEN')
  dp = Dispatcher()


  @dp.message(text='/start')
  async def start_command(message: Message):
      kb = ReplyKeyboardMarkup()
      button = KeyboardButton(text='BUTTON')
      kb.add_button(button)
      await message.answer(text='Hello World!', reply_markup=kb)


  @dp.callback_query(data='data')
  async def some_func(callback: CallbackQuery):
      await callback.answer(text='Hello World!', show_alert=True)


  async def main():
      await bot.skip_updates()
      await dp.start_polling(bot)


  if __name__ == '__main__':
      asyncio.run(main())

**Developer - Blaze Egor**