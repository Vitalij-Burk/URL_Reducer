from redis.asyncio import Redis

from src.users.core.interfaces.repositories.units_of_work.cache import IUnitOfWork
from src.users.infrastructure.storages.cache.repository import UserRepository


class UnitOfWork(IUnitOfWork):
    def __init__(self, client: Redis):
        self.client = client
        self.users = UserRepository(client)
        self._pipeline = None

    async def start_pipeline(self):
        self._pipeline = self.client.pipeline()
        return self._pipeline

    async def execute_pipeline(self):
        if self._pipeline:
            result = await self._pipeline.execute()
            self._pipeline = None
            return result
        return None

    async def discard_pipeline(self):
        if self._pipeline:
            await self._pipeline.discard()
            self._pipeline = None

    async def clear_cache(self, pattern: str = "*"):
        keys = self.client.keys(pattern)
        if keys:
            await self.client.delete(*keys)

    async def get_cache_info(self) -> dict:
        info = await self.client.info()
        return {
            "used_memory": info.get("used_memory_human"),
            "connected_clients": info.get("connected_clients"),
            "keyspace_hits": info.get("keyspace_hits"),
            "keyspace_misses": info.get("keyspace_misses"),
        }

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._pipeline and exc_type:
            await self.discard_pipeline()
        elif self._pipeline:
            await self.execute_pipeline()
