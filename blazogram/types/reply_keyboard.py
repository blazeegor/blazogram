import json
from dataclasses import dataclass
from ..exceptions import KeyboardError
from .chat import ChatAdministratorRights


@dataclass
class KeyboardButtonRequestUser:
    request_id: int
    user_is_bot: bool = False
    user_is_premium: bool = False


@dataclass
class KeyboardButtonRequestChat:
    request_id: int
    chat_is_channel: bool
    chat_is_forum: bool = False
    chat_has_username: bool = False
    chat_is_created: bool = False
    user_administrator_rights: ChatAdministratorRights = None
    bot_administrator_rights: ChatAdministratorRights = None
    bot_is_member: bool = False


@dataclass
class KeyboardButton:
    text: str
    request_user: KeyboardButtonRequestUser = None
    request_chat: KeyboardButtonRequestChat = None
    request_contact: bool = False
    request_location: bool = False


def get_button_dict(button: KeyboardButton) -> dict:
    button_dict = dict(text=button.text, request_contact=button.request_contact,
                       request_location=button.request_location)

    if button.request_user:
        button_dict['request_user'] = button.request_user

    if button.request_chat:
        button_dict['request_chat'] = button.request_chat

    return button_dict


class KeyboardLine:
    def __init__(self, *buttons: KeyboardButton):
        self.buttons = list(buttons)

    def add_buttons(self, *buttons: KeyboardButton):
        self.buttons.extend(buttons)

    def __len__(self) -> int:
        return len(self.buttons)

    def __iter__(self):
        self.iter_buttons = iter(self.buttons)
        return self

    def __next__(self):
        return self.iter_buttons.__next__()


class Keyboard:
    def __init__(self, *lines: KeyboardLine):
        self.lines = list(lines)

    def add_lines(self, *lines: KeyboardLine):
        self.lines.extend(lines)

    def __iter__(self):
        self.iter_lines = iter(self.lines)
        return self

    def __next__(self):
        return self.iter_lines.__next__()


class ReplyKeyboardMarkup:
    def __init__(self, keyboard: Keyboard = None, row_width: int = 3,
                 resize_keyboard: bool = True, one_time_keyboard: bool = False,
                 selective: bool = None, input_field_placeholder: str = None):

        self.row_width = row_width
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
        self.selective = selective
        self.input_field_placeholder = input_field_placeholder

        if keyboard:
            for line in keyboard:
                if len(line) > row_width:
                    raise KeyboardError(message='The number of buttons in a line cannot be more row width.')

            self.buttons = [[get_button_dict(button) for button in line] for line in keyboard]
        else:
            self.buttons = [[]]

    @property
    def reply_markup(self):
        reply_markup = {'keyboard': self.buttons,
                        'resize_keyboard': self.resize_keyboard,
                        'one_time_keyboard': self.one_time_keyboard}

        if self.input_field_placeholder:
            reply_markup['input_field_placeholder'] = self.input_field_placeholder

        if self.selective:
            reply_markup['selective'] = self.selective

        return json.dumps(reply_markup)

    def add_button(self, button: KeyboardButton):
        button_dict = get_button_dict(button)
        if len(self.buttons[-1]) >= self.row_width:
            self.buttons.append([button_dict])
        else:
            self.buttons[-1].append(button_dict)

    def add_buttons(self, *buttons: KeyboardButton, is_row: bool = False):
        if is_row:
            self.buttons.append([get_button_dict(button) for button in buttons])
        else:
            for button in buttons:
                self.add_button(button)


class ReplyKeyboardRemove:
    reply_markup = json.dumps({'remove_keyboard': True})