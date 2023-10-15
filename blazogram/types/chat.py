from dataclasses import dataclass
from .photo import ChatPhoto


@dataclass
class Chat:
    id: int
    type: str
    title: str = None
    username: str = None
    first_name: str = None
    last_name: str = None
    is_forum: bool = None
    bio: str = None
    photo: ChatPhoto = None