from dataclasses import dataclass
from ..state import State
from typing import Optional


@dataclass
class UserKey:
    bot_id: int
    chat_id: int
    user_id: int


class BaseStorage:
    def add_key(self, key: UserKey):
        pass

    async def set_state(self, key: UserKey, state: State) -> None:
        pass

    async def get_state(self, key: UserKey) -> State:
        pass

    async def get_data(self, key: UserKey) -> dict:
        pass

    async def set_data(self, key: UserKey, data: dict) -> dict:
        pass

    async def update_data(self, key: UserKey, data: dict) -> dict:
        current_data = await self.get_data(key=key)
        current_data.update(data)
        await self.set_data(key=key, data=current_data)
        return current_data.copy()

    async def clear(self, key: UserKey) -> None:
        pass