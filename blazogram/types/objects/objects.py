from dataclasses import dataclass


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