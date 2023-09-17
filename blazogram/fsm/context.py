from .storage.base import BaseStorage, UserKey
from .state import State


class FSMContext:
    def __init__(self, key: UserKey, storage: BaseStorage):
        self.key = key
        self.storage = storage

    async def set_state(self, state: State) -> None:
        return await self.storage.set_state(key=self.key, state=state)

    async def get_state(self) -> State:
        return await self.storage.get_state(key=self.key)

    async def get_data(self) -> dict:
        return await self.storage.get_data(self.key)

    async def set_data(self, data: dict) -> dict:
        return await self.storage.set_data(key=self.key, data=data)

    async def update_data(self, **data) -> dict:
        return await self.storage.update_data(key=self.key, data=data)

    async def clear(self) -> None:
        return await self.storage.clear(key=self.key)