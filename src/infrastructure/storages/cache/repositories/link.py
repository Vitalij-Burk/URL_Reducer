import json
from typing import Optional
from uuid import UUID

from redis.asyncio import Redis

from src.core.domain.schemas.inner.link import LinkResponseInner
from src.core.repositories.cache.link import ILinkCacheRepository
from src.infrastructure.storages.cache.dal.link import LinkDAL


class LinkRepository(ILinkCacheRepository):
    def __init__(self, client: Redis, pipeline: Optional[Redis] = None):
        self.client = client
        self.pipeline = pipeline
        self.link_dal = LinkDAL(pipeline or client)

    async def cache_by_id(self, id: UUID, entity: LinkResponseInner):
        cache_key = f"link:{id}"
        cache_data = entity.model_dump_json()
        resp = await self.link_dal.create(cache_key, cache_data)
        return resp

    async def get_by_id(self, id: UUID) -> LinkResponseInner | None:
        cache_key = f"link:{id}"
        resp = await self.link_dal.get(cache_key)
        if resp:
            return LinkResponseInner(**json.loads(resp))
        return None

    async def delete_by_id(self, id: UUID):
        cache_key = f"link:{id}"
        await self.link_dal.delete(cache_key)

    async def cache_by_reduced(self, reduced: str, entity: LinkResponseInner):
        cache_key = f"link:{reduced}"
        cache_data = entity.model_dump_json()
        resp = await self.link_dal.create(cache_key, cache_data)
        return resp

    async def get_by_reduced(self, reduced: str) -> LinkResponseInner | None:
        cache_key = f"link:{reduced}"
        resp = await self.link_dal.get(cache_key)
        if resp:
            return LinkResponseInner(**json.loads(resp))
        return None

    async def delete_by_reduced(self, reduced: str):
        cache_key = f"link:{reduced}"
        await self.link_dal.delete(cache_key)
