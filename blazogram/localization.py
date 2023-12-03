from aiotrans import Translaitor
from .enums import Languages


class BlazeLocale:
    def __init__(self):
        self.users: dict[int, str] = dict()
        self.translator = Translaitor()

    def set_language(self, user_id: int, language: Languages) -> None:
        self.users[user_id] = language.value

    def get_language(self, user_id: int) -> str:
        return self.users[user_id]

    def check_user(self, user_id: int) -> bool:
        return user_id in self.users

    async def translate(self, user_id: int, text: str, source: Languages) -> str:
        translation = await self.translator.translate(
            text, target=self.get_language(user_id), source=source.value
        )

        return translation
