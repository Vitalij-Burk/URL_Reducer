import json
from uuid import UUID

from core.repositories.DAL.redis.redisDAL import RedisDAL
from db.models import User
from fastapi.encoders import jsonable_encoder
from redis.asyncio import Redis


class UserCacheProducer:
    def __init__(self, redis_client: Redis):
        self.redis_user_dal = RedisDAL(redis_client=redis_client)

    async def _cache_user(self, user: User, time: int = 600):
        cache_key = f"user:{user.user_id}"
        return await self.redis_user_dal.cache(
            cache_key,
            json.dumps(jsonable_encoder(user)),
            time,
        )

    async def _get_user_from_cache(self, user_id: UUID):
        cache_key = f"user:{user_id}"
        if cached_data := await self.redis_user_dal.get(cache_key):
            return json.loads(cached_data)

    async def _delete_user_from_cache(self, user_id: UUID):
        cache_key = f"user:{user_id}"
        return await self.redis_user_dal.delete(cache_key)

    async def update_user_in_cache(
        self, user_id: UUID, updated_user: User, time: int = 600
    ):
        cache_key = f"user:{user_id}"
        await self.redis_user_dal.delete(cache_key)
        return await self.redis_user_dal.cache(
            cache_key,
            json.dumps(jsonable_encoder(updated_user)),
            time,
        )
