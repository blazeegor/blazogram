from googletrans import Translator
from .enums import Languages
from dataclasses import dataclass


@dataclass(frozen=True)
class UserLanguage:
    user_id: int
    language: str


class BlazeLocale:
    def __init__(self):
        self.users: dict[int, UserLanguage] = {}
        self.translator = Translator()

    def set_language(self, user_id: int, language: Languages) -> None:
        self.users[user_id] = UserLanguage(user_id, language.name)

    def get_language(self, user_id: int) -> str:
        return self.users[user_id].language

    def check_user(self, user_id: int) -> bool:
        return user_id in self.users

    def translate(self, user_id: int, text: str) -> str:
        translation = self.translator.translate(text, dest=self.get_language(user_id)).text

        return translation
