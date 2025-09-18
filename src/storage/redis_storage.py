from typing import Any

from aiogram.fsm.storage.redis import RedisStorage as AiogramRedisStorage
from redis.asyncio.client import Redis

from src.storage import BaseStorage


class RedisStorage(BaseStorage, AiogramRedisStorage):
    def __init__(self, redis: Redis, *args, **kwargs):
        super().__init__(redis=redis, *args, **kwargs)

    async def lock(self, name: str, timeout: int = 5) -> bool:
        lock_key = self.__generate_lock_key(name)
        acquired = await self.redis.set(
            lock_key,
            "locked",
            nx=True,
            ex=timeout
        )
        return acquired is not None

    async def unlock(self, name: str) -> None:
        lock_key = self.__generate_lock_key(name)
        await self.redis.delete(lock_key)

    async def get(self, name: str, version: int = 0) -> Any | None:
        key = self.__generate_key(name, version)
        return await self.redis.get(key)

    async def set(self, name: str, value: Any, version: int = 0) -> None:
        key = self.__generate_key(name, version)
        await self.redis.set(key, value)

    async def delete(self, name: str, version: int = 0) -> None:
        key = self.__generate_key(name, version)
        await self.redis.delete(key)

    def __generate_key(self, name: str, version: int) -> str:
        return f"{name}:{version}"

    def __generate_lock_key(self, name: str) -> str:
        return f"{name}:lock"
