from dataclasses import dataclass
from ..state import State
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class UserKey:
    chat_id: int
    user_id: int


class BaseStorage(ABC):
    @abstractmethod
    async def set_state(self, key: UserKey, state: State) -> None:
        pass

    @abstractmethod
    async def get_state(self, key: UserKey) -> State:
        pass

    @abstractmethod
    async def get_data(self, key: UserKey) -> dict:
        pass

    @abstractmethod
    async def set_data(self, key: UserKey, data: dict) -> dict:
        pass

    @abstractmethod
    async def update_data(self, key: UserKey, data: dict) -> dict:
       pass

    @abstractmethod
    async def clear(self, key: UserKey) -> None:
        pass