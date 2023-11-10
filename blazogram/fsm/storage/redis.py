from .base import BaseStorage, UserKey
from ..state import State
from redis.asyncio.client import Redis, ConnectionPool
from typing import Literal, Optional
import json


def build_key(key: UserKey, build_name: Literal['state', 'data']) -> str:
    redis_key = 'USER' + build_name + str(key.chat_id) + ':' + str(key.user_id)
    return redis_key


class RedisStorage(BaseStorage):
    def __init__(self, redis: Redis = None, host: str = 'localhost', port: int = 6379, db: int = 0, password: str = None):
        self.redis = Redis(host=host, port=port, db=db, password=password) if not redis else redis

    @classmethod
    def from_url(cls, url: str):
        pool = ConnectionPool.from_url(url=url)
        redis = Redis(connection_pool=pool)
        return cls(redis=redis)

    async def set_state(self, key: UserKey, state: Optional[State]) -> None:
        await self.redis.set(name=build_key(key, 'state'), value=state.__str__())

    async def get_state(self, key: UserKey) -> State:
        value = (await self.redis.get(name=build_key(key, 'state'))).decode('utf-8')
        if value == 'None':
            value = None
        return value

    async def set_data(self, key: UserKey, data: dict) -> dict:
        await self.redis.set(name=build_key(key, 'data'), value=json.dumps(data))
        return data.copy()

    async def get_data(self, key: UserKey) -> dict:
        value = await self.redis.get(name=build_key(key, 'data'))
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