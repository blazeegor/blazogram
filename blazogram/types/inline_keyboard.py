import json
from dataclasses import dataclass
from ..exceptions import KeyboardError


@dataclass
class InlineKeyboardButton:
    text: str
    callback_data: str = None
    url: str = None


class InlineButtonsLine:
    def __init__(self, *buttons: InlineKeyboardButton):
        self.buttons = list(buttons)


def get_button(button: InlineKeyboardButton) -> dict:
    but = {'text': button.text}
    param = {'callback_data': button.callback_data} if button.callback_data else {'url': button.url}
    but.update(param)
    return but


class InlineKeyboardMarkup:
    def __init__(self, inline_keyboard: list[InlineButtonsLine] = None, row_width: int = 3):
        self.row_width = row_width
        if inline_keyboard:
            for line in inline_keyboard:
                if len(line.buttons) > row_width:
                    raise KeyboardError(message='The number of buttons in a line cannot be more row width.')

            self.buttons = [[get_button(button) for button in line.buttons] for line in inline_keyboard]
        else:
            self.buttons = [[]]

    @property
    def reply_markup(self) -> str:
        return json.dumps({'inline_keyboard': self.buttons})

    def add_button(self, button: InlineKeyboardButton):
        if button.callback_data and button.url:
            raise KeyboardError(message='Inline Keyboard Button must to have a callback_data or url.')

        button_dict = get_button(button)
        if len(self.buttons[-1]) >= self.row_width:
            self.buttons.append([button_dict])
        else:
            self.buttons[-1].append(button_dict)

    def add_buttons(self, *buttons: InlineKeyboardButton, is_row: bool = False):
        if is_row:
            self.buttons.append([get_button(button) for button in buttons])
        else:
            for button in buttons:
                self.add_button(button)