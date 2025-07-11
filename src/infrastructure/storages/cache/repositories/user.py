import json
from typing import Optional
from uuid import UUID

from pydantic import EmailStr
from redis.asyncio import Redis

from src.core.domain.schemas.inner.user import UserResponseInner
from src.core.repositories.cache.user import IUserCacheRepository
from src.infrastructure.storages.cache.dal.user import UserDAL


class UserRepository(IUserCacheRepository):
    def __init__(self, client: Redis, pipeline: Optional[Redis] = None):
        self.client = client
        self.pipeline = pipeline
        self.user_dal = UserDAL(pipeline or client)

    async def cache_by_id(self, id: UUID, entity: UserResponseInner):
        cache_key = f"user:{id}"
        cache_data = entity.model_dump_json()
        resp = await self.user_dal.create(cache_key, cache_data)
        return resp

    async def get_by_id(self, id: UUID) -> UserResponseInner:
        cache_key = f"user:{id}"
        resp = await self.user_dal.get(cache_key)
        if resp:
            return UserResponseInner(**json.loads(resp))
        return None

    async def delete_by_id(self, id: UUID):
        cache_key = f"user:{id}"
        await self.user_dal.delete(cache_key)

    async def cache_by_email(self, email: EmailStr, entity: UserResponseInner):
        cache_key = f"user:{email}"
        cache_data = entity.model_dump_json()
        resp = await self.user_dal.create(cache_key, cache_data)
        return resp

    async def get_by_email(self, email: EmailStr) -> UserResponseInner:
        cache_key = f"user:{email}"
        resp = await self.user_dal.get(cache_key)
        if resp:
            return UserResponseInner(**json.loads(resp))
        return None

    async def delete_by_email(self, email: EmailStr):
        cache_key = f"user:{email}"
        await self.user_dal.delete(cache_key)
