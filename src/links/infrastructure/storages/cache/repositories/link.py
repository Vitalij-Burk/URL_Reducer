from typing import Optional
from uuid import UUID

from redis.asyncio import Redis

from src.links.core.base_componenets.repositories.link.cache import ILinkCacheRepository
from src.links.core.domain.schemas.inner.link import LinkResponseInner
from src.links.core.utils.serializers.link.cache.out import deserialize_link_from_cache
from src.links.core.utils.serializers.link.cache.to import serialize_link_to_cache
from src.links.infrastructure.storages.cache.base.DAL.link import LinkDAL


class LinkRepository(ILinkCacheRepository):
    def __init__(self, client: Redis, pipeline: Optional[Redis] = None):
        self.client = client
        self.pipeline = pipeline
        self.link_dal = LinkDAL(pipeline or client)

    async def cache_by_id(self, id: UUID, entity: LinkResponseInner):
        cache_key = f"link:{id}"
        cache_data = serialize_link_to_cache(entity)
        resp = await self.link_dal.create(cache_key, cache_data)
        return resp

    async def get_by_id(self, id: UUID) -> LinkResponseInner | None:
        cache_key = f"link:{id}"
        resp = await self.link_dal.get(cache_key)
        if resp:
            return deserialize_link_from_cache(resp)
        return None

    async def delete_by_id(self, id: UUID):
        cache_key = f"link:{id}"
        await self.link_dal.delete(cache_key)

    async def cache_by_short_code(self, short_code: str, entity: LinkResponseInner):
        cache_key = f"link:{short_code}"
        cache_data = serialize_link_to_cache(entity)
        resp = await self.link_dal.create(cache_key, cache_data)
        return resp

    async def get_by_short_code(self, short_code: str) -> LinkResponseInner | None:
        cache_key = f"link:{short_code}"
        resp = await self.link_dal.get(cache_key)
        if resp:
            return deserialize_link_from_cache(resp)
        return None

    async def delete_by_short_code(self, short_code: str):
        cache_key = f"link:{short_code}"
        await self.link_dal.delete(cache_key)
