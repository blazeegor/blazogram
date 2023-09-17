from .base import BaseStorage, UserKey
from ..state import State
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class StorageRecord:
    state: State = None
    data: dict = field(default_factory=dict)


class MemoryStorage(BaseStorage):
    def __init__(self):
        self.storage: defaultdict[UserKey, StorageRecord] = defaultdict(StorageRecord)

    async def set_state(self, key: UserKey, state: State) -> None:
        self.storage[key].state = state

    async def get_state(self, key: UserKey) -> State:
        return self.storage[key].state

    async def get_data(self, key: UserKey) -> dict:
        return self.storage[key].data

    async def set_data(self, key: UserKey, data: dict) -> dict:
        self.storage[key].data = data
        return data.copy()

    async def update_data(self, key: UserKey, data: dict) -> dict:
        current_data = await self.get_data(key=key)
        current_data.update(data)
        await self.set_data(key=key, data=current_data)
        return current_data.copy()

    async def clear(self, key: UserKey) -> None:
        self.storage[key].state = None
        self.storage[key].data = {}