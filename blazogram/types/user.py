from dataclasses import dataclass


@dataclass
class User:
    id: int
    is_bot: bool
    username: str
    first_name: str
    last_name: str = None

    @property
    def full_name(self) -> str:
        return self.first_name + ' ' + self.last_name