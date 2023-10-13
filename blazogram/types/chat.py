from dataclasses import dataclass


@dataclass
class Chat:
    id: int
    type: str
    username: str
    first_name: str