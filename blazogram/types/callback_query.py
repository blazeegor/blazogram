from ..types.user import User
from ..types.message import Message


class CallbackQuery:
    def __init__(self, bot, callback_query_id: int, data: str, message: Message, user: User):
        self.message = message
        self.bot = bot
        self.callback_query_id = callback_query_id
        self.from_user = User(id=user.id, first_name=user.first_name, username=user.username)
        self.data = data

    async def answer(self, text: str, show_alert: bool = False):
        return await self.bot.answer_callback_query(self.callback_query_id, text, show_alert)