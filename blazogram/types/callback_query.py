from .objects import User
from .message import Message


class CallbackQuery:
    def __init__(self, bot, callback_query_id: int, data: str, user: User, message: Message):
        self.bot = bot
        self.callback_query_id = callback_query_id
        self.data = data
        self.from_user = user
        self.message = message

    async def answer(self, text: str, show_alert: bool = False):
        return await self.bot.answer_callback_query(self.callback_query_id, text=text, show_alert=show_alert)