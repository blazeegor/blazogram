from googletrans import Translator
from .enums import Languages
from dataclasses import dataclass


@dataclass
class UserLanguage:
    user_id: int
    language: str


class BlazeLocale:
    def __init__(self):
        self.users: list[UserLanguage] = []
        self.translator = Translator()

    def set_language(self, user_id: int, language: Languages):
        for user in self.users:
            if user.user_id == user_id:
                self.users.remove(user)
                self.users.append(UserLanguage(user_id, language.name))
                return
        self.users.append(UserLanguage(user_id, language.name))

    def get_language(self, user_id: int):
        for user in self.users:
            if user.user_id == user_id:
                return user.language

    def check_user(self, user_id: int):
        for user in self.users:
            if user.user_id == user_id:
                return True
        return False

    def translate(self, user_id: int, text: str) -> str:
        translation = (self.translator.translate(text, dest=self.get_language(user_id))).text
        return translation