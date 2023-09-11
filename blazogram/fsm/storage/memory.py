from .base import BaseStorage, UserKey
from ..state import State


def build_key(key: UserKey) -> str:
    return f'{key.bot_id}:{key.chat_id}:{key.user_id}'


class MemoryStorage(BaseStorage):
    def __init__(self):
        self.storage = dict()

    def add_key(self, key: UserKey):
        key_str = build_key(key)
        if key_str not in self.storage.keys():
            self.storage[key_str] = dict(state=None, data={})

    async def set_state(self, key: UserKey, state: State) -> None:
        key_str = build_key(key)
        self.storage[key_str]['state'] = state.state_id

    async def get_state(self, key: UserKey) -> int:
        key_str = build_key(key)
        return self.storage[key_str]['state']

    async def get_data(self, key: UserKey) -> dict:
        return self.storage[build_key(key)]['data']

    async def set_data(self, key: UserKey, data: dict) -> dict:
        self.storage[build_key(key)]['data'] = data
        return data

    async def update_data(self, key: UserKey, data: dict) -> dict:
        current_data = await self.get_data(key=key)
        current_data.update(data)
        await self.set_data(key=key, data=data)
        return current_data.copy()

    async def clear(self, key: UserKey) -> None:
        key_str = build_key(key)
        self.storage[key_str]['state'] = None
        self.storage[key_str]['data'] = {}