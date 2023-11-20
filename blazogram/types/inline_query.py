from dataclasses import dataclass
from .user import User
from .location import Location


@dataclass
class InlineQuery:
    id: str
    from_user: User
    query: str
    offset: str
    chat_type: str = None
    location: Location = None
