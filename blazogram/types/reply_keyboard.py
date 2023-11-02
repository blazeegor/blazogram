import json
from dataclasses import dataclass
from ..exceptions import KeyboardError


@dataclass
class KeyboardButton:
    text: str


class ButtonsLine:
    def __init__(self, *buttons: KeyboardButton):
        self.buttons = list(buttons)


class ReplyKeyboardMarkup:
    def __init__(self, keyboard: list[ButtonsLine] = None, row_width: int = 3, resize_keyboard: bool = True, one_time_keyboard: bool = False):
        self.row_width = row_width
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard

        if keyboard:
            for line in keyboard:
                if len(line.buttons) > row_width:
                    raise KeyboardError(message='The number of buttons in a line cannot be more row width.')

            self.buttons = [line.buttons for line in keyboard]
        else:
            self.buttons = [[]]

    @property
    def reply_markup(self):
        return json.dumps({'keyboard': self.buttons, 'resize_keyboard': self.resize_keyboard, 'one_time_keyboard': self.one_time_keyboard})

    def add_button(self, button: KeyboardButton):
        button_dict = {'text': button.text}
        if len(self.buttons[-1]) == self.row_width:
            self.buttons.append([button_dict])
        else:
            self.buttons[-1].append(button_dict)

    def add_buttons(self, *buttons: KeyboardButton, is_row: bool = False):
        if is_row:
            self.buttons.append(list(buttons))
        else:
            for button in buttons:
                self.add_button(button)


class ReplyKeyboardRemove:
    reply_markup = json.dumps({'remove_keyboard': True})