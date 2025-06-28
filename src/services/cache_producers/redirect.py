import json

from core.repositories.DAL.redis.redisDAL import RedisDAL
from db.models import Link
from fastapi.encoders import jsonable_encoder
from redis.asyncio import Redis


class RedirectCacheProducer:
    def __init__(self, redis_client: Redis):
        self.redis_link_dal = RedisDAL(redis_client=redis_client)

    async def _cache_link(self, link: Link, time: int = 600):
        cache_key = f"short_link:{link.short_link}"
        return await self.redis_link_dal.cache(
            cache_key,
            json.dumps(jsonable_encoder(link)),
            time,
        )

    async def _get_link_from_cache(self, short_link: str):
        cache_key = f"short_link:{short_link}"
        if cached_data := await self.redis_link_dal.get(cache_key):
            return json.loads(cached_data)

    async def _delete_link_from_cache(self, short_link: str):
        cache_key = f"short_link:{short_link}"
        return await self.redis_link_dal.delete(cache_key)

    async def update_link_in_cache(self, updated_link: Link, time: int = 600):
        cache_key = f"short_link:{updated_link.short_link}"
        await self.redis_link_dal.delete(cache_key)
        return await self.redis_link_dal.cache(
            cache_key,
            json.dumps(jsonable_encoder(updated_link)),
            time,
        )
