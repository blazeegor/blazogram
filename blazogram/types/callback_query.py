from .objects import User
from .message import Message


class CallbackQuery:
    def __init__(self, bot, callback_query_id: int, data: str, user: User, message: Message):
        self.bot = bot
        self.callback_query_id = callback_query_id
        self.from_user = User(id=user.id, is_bot=user.is_bot, first_name=user.first_name, last_name=user.last_name, username=user.username)
        self.message = message
        self.data = data

    async def answer(self, text: str, show_alert: bool = False):
        return await self.bot.answer_callback_query(self.callback_query_id, text, show_alert)