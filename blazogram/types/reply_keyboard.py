import json
from dataclasses import dataclass


@dataclass
class KeyboardButton:
    text: str


class ReplyKeyboardMarkup:
    def __init__(self, resize_keyboard: bool = True, one_time_keyboard: bool = False):
        self.buttons = []
        self.reply_markup = json.dumps({'keyboard': self.buttons, 'resize_keyboard': resize_keyboard, 'one_time_keyboard': one_time_keyboard})

    def add_button(self, button: KeyboardButton):
        self.buttons.append([{'text': button.text}])
        reply_markup = json.loads(self.reply_markup)
        reply_markup['keyboard'] = self.buttons
        self.reply_markup = json.dumps(reply_markup)

    def add_buttons(self, *buttons: KeyboardButton):
        for button in buttons:
            self.add_button(button)


class ReplyKeyboardRemove:
    reply_markup = json.dumps({'remove_keyboard': True})
