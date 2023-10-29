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
    def __init__(self, inline_keyboard: list[[InlineKeyboardButton]] = None):
        self.buttons: list[[InlineKeyboardButton]] = [] if not inline_keyboard else [get_button(but[0]) for but in inline_keyboard]

    @property
    def reply_markup(self) -> str:
        return json.dumps({'inline_keyboard': self.buttons})

    def add_button(self, button: InlineKeyboardButton):
        if button.url is not None and button.callback_data is None or button.url is None and button.callback_data is not None:
            button = get_button(button)
            self.buttons.append([button])
        else:
            raise ValueError('Inline Keyboard Button must to have a callback_data or url.')

    def add_buttons(self, *buttons: InlineKeyboardButton):
        for button in buttons:
            self.add_button(button)
