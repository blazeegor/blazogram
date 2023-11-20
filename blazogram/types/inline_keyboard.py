import json
from dataclasses import dataclass
from ..exceptions import KeyboardError


@dataclass
class InlineKeyboardButton:
    text: str
    callback_data: str = None
    url: str = None


def get_button_dict(button: InlineKeyboardButton) -> dict:
    button_dict = {"text": button.text}

    if button.callback_data:
        button_dict["callback_data"] = button.callback_data

    if button.url:
        button_dict["url"] = button.url

    return button_dict


class InlineKeyboardLine:
    def __init__(self, *buttons: InlineKeyboardButton):
        self.buttons = list(buttons)

    def add_buttons(self, *buttons: InlineKeyboardButton):
        self.buttons.extend(buttons)

    def __len__(self) -> int:
        return len(self.buttons)

    def __iter__(self):
        self.iter_buttons = iter(self.buttons)
        return self

    def __next__(self):
        return self.iter_buttons.__next__()


class InlineKeyboard:
    def __init__(self, *lines: InlineKeyboardLine):
        self.lines = list(lines)

    def add_lines(self, *lines: InlineKeyboardLine):
        self.lines.extend(lines)

    def __iter__(self):
        self.iter_lines = iter(self.lines)
        return self

    def __next__(self):
        return self.iter_lines.__next__()


class InlineKeyboardMarkup:
    def __init__(self, inline_keyboard: InlineKeyboard = None, row_width: int = 3):
        self.row_width = row_width

        if inline_keyboard:
            for line in inline_keyboard:
                if len(line) > row_width:
                    raise KeyboardError(
                        message="The number of buttons in a line cannot be more row width."
                    )

            self.buttons = [
                [get_button_dict(button) for button in line] for line in inline_keyboard
            ]
        else:
            self.buttons = [[]]

    @property
    def reply_markup(self) -> str:
        return json.dumps({"inline_keyboard": self.buttons})

    def add_button(self, button: InlineKeyboardButton):
        if button.callback_data and button.url:
            raise KeyboardError(
                message="Inline Keyboard Button must to have a callback_data or url."
            )

        button_dict = get_button_dict(button)
        if len(self.buttons[-1]) >= self.row_width:
            self.buttons.append([button_dict])
        else:
            self.buttons[-1].append(button_dict)

    def add_buttons(self, *buttons: InlineKeyboardButton, is_row: bool = False):
        if is_row:
            self.buttons.append([get_button_dict(button) for button in buttons])
        else:
            for button in buttons:
                self.add_button(button)
