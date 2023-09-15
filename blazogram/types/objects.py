from dataclasses import dataclass
from aiohttp import FormData


@dataclass
class Chat:
    id: int
    type: str
    username: str
    first_name: str


@dataclass
class User:
    id: int
    is_bot: bool
    first_name: str
    username: str


@dataclass
class PhotoSize:
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: int


class InputFile:
    def __init__(self, filename: str):
        self.data = FormData()
        self.file = open(filename, 'rb')
        self.data.add_field('photo', value=self.file, filename=filename, content_type='multipart/form-data')