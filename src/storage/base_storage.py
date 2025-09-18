from typing import Any


class BaseStorage:
    async def lock(self, name: str, timeout: int = 5) -> bool:
        raise NotImplementedError

    async def unlock(self, name: str):
        raise NotImplementedError

    async def get(self, name: str, version: int) -> Any | None:
        raise NotImplementedError

    async def set(self, name: str, value: Any, version: int):
        raise NotImplementedError

    async def delete(self, name):
        raise NotImplementedError