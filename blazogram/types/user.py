from dataclasses import dataclass


@dataclass
class User:
    id: int
    first_name: str
    username: str