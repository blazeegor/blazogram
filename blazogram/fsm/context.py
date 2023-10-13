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
        current_data = await self.get_data()
        current_data.update(data)
        await self.set_data(current_data)
        return current_data.copy()

    async def clear(self) -> None:
        await self.set_state(state=None)
        await self.set_data(data={})