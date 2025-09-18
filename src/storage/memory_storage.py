from typing import Any

from src.storage import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage as AiogramMemoryStorage


class MemoryStorage(BaseStorage, AiogramMemoryStorage):
    __storage: dict[str, Any] = {}

    async def lock(self, name: str, timeout: int = 5) -> bool:
        lock_key = self.__generate_lock_key(name)
        if lock_key in self.__storage:
            return False

        self.__storage[lock_key] = True
        return True

    async def unlock(self, name: str):
        return await self.delete(self.__generate_lock_key(name))

    async def delete(self, name: str):
        del self.__storage[name]

    async def set(self, name: str, value: Any, version: int):
        self.__storage[self.__generate_key(name, version)]= value

    async def get(self, name: str, version: int) -> Any | None:
        return self.__storage.get(self.__generate_key(name, version), None)

    def __generate_key(self, name: str, version: int) -> str:
        return f"{name}:{version}"

    def __generate_lock_key(self, name: str) -> str:
        return f"{name}.lock"
