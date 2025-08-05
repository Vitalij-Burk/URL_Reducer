from redis.asyncio import Redis

from src.core.domain.settings import Config


class UserDAL:
    def __init__(self, client: Redis):
        self.client = client

    async def create(self, key: str, user):
        return await self.client.set(key, user, Config.REDIS_DEFAULT_TTL)

    async def get(self, key: str):
        return await self.client.get(key)

    async def delete(self, key: str):
        return await self.client.delete(key)
