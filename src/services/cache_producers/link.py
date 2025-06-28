import json
from uuid import UUID

from core.repositories.DAL.redis.redisDAL import RedisDAL
from db.models import Link
from fastapi.encoders import jsonable_encoder
from redis.asyncio import Redis


class LinkCacheProducer:
    def __init__(self, redis_client: Redis):
        self.redis_link_dal = RedisDAL(redis_client=redis_client)

    async def _cache_link(self, link: Link, time: int = 600):
        cache_key = f"link:{link.link_id}"
        return await self.redis_link_dal.cache(
            cache_key,
            json.dumps(jsonable_encoder(link)),
            time,
        )

    async def _get_link_from_cache(self, link_id: UUID):
        cache_key = f"link:{link_id}"
        if cached_data := await self.redis_link_dal.get(cache_key):
            return json.loads(cached_data)

    async def _delete_link_from_cache(self, link_id: UUID):
        cache_key = f"link:{link_id}"
        return await self.redis_link_dal.delete(cache_key)

    async def update_link_in_cache(
        self, link_id: UUID, updated_link: Link, time: int = 600
    ):
        cache_key = f"link:{link_id}"
        await self.redis_link_dal.delete(cache_key)
        return await self.redis_link_dal.cache(
            cache_key,
            json.dumps(jsonable_encoder(updated_link)),
            time,
        )
