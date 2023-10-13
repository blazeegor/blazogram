import json
from dataclasses import dataclass


@dataclass
class InlineKeyboardButton:
    text: str
    callback_data: str = None
    url: str = None


def get_button(button: InlineKeyboardButton):
    but = {'text': button.text}
    param = {'callback_data': button.callback_data} if button.callback_data else {'url': button.url}
    but.update(param)
    return but


class InlineKeyboardMarkup:
    def __init__(self):
        self.buttons = []
        self.reply_markup = json.dumps({'inline_keyboard': self.buttons})

    def add_button(self, button: InlineKeyboardButton):
        if button.url is not None and button.callback_data is None or button.url is None and button.callback_data is not None:
            button = get_button(button)
            self.buttons.append([button])
            reply_markup = json.loads(self.reply_markup)
            reply_markup['inline_keyboard'] = self.buttons
            self.reply_markup = json.dumps(reply_markup)
        else:
            raise ValueError('Inline Keyboard Button must to have a callback_data or url.')

    def add_buttons(self, *buttons: InlineKeyboardButton):
        for button in buttons:
            self.add_button(button)