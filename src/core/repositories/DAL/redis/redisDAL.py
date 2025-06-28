from redis.asyncio import Redis


class RedisDAL:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    async def cache(self, cache_key: str, data: any, time: int):
        return await self.redis_client.set(
            cache_key,
            data,
            time,
        )

    async def get(self, cache_key: str):
        if cached_data := await self.redis_client.get(cache_key):
            return cached_data

    async def delete(self, cache_key: str):
        return await self.redis_client.delete(cache_key)
