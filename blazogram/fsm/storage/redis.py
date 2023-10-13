from .base import BaseStorage, UserKey
from ..state import State
from redis.asyncio.client import Redis, ConnectionPool
from typing import Literal
import json


class KeyBuilder:
    def build(self, key: UserKey, build_name: Literal['state', 'data']) -> str:
        redis_key = 'USER' + build_name + str(key.chat_id) + ':' + str(key.user_id)
        return redis_key


class RedisStorage(BaseStorage):
    def __init__(self, redis: Redis):
        self.redis = redis
        self.key_builder = KeyBuilder()

    @classmethod
    def from_url(cls, url: str):
        pool = ConnectionPool.from_url(url=url)
        redis = Redis(connection_pool=pool)
        return cls(redis=redis)

    async def set_state(self, key: UserKey, state: State) -> None:
        await self.redis.set(name=self.key_builder.build(key, 'state'), value=state.__str__())

    async def get_state(self, key: UserKey) -> State:
        value = (await self.redis.get(name=self.key_builder.build(key, 'state'))).decode('utf-8')
        if value == 'None':
            value = None
        return value

    async def set_data(self, key: UserKey, data: dict) -> dict:
        await self.redis.set(name=self.key_builder.build(key, 'data'), value=json.dumps(data))
        return data.copy()

    async def get_data(self, key: UserKey) -> dict:
        value = await self.redis.get(name=self.key_builder.build(key, 'data'))
        if isinstance(value, bytes):
            value = value.decode('utf-8')
            if value == 'None':
                value = json.dumps({})
        else:
            value = json.dumps({})
        data = json.loads(value)
        return data

    async def close(self):
        await self.redis.close()