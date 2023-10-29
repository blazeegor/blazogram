from dataclasses import dataclass


@dataclass
class PhotoSize:
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: int


@dataclass
class ChatPhoto:
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str
