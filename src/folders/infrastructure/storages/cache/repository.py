from typing import Optional
from uuid import UUID

from redis.asyncio import Redis

from src.folders.core.base_componenets.repositories.cache import (
    IFolderCacheRepository,
)
from src.folders.core.domain.schemas.inner.folder import FolderResponseInner
from src.folders.core.utils.serializers.folder.cache.out import (
    deserialize_folder_from_cache,
)
from src.folders.core.utils.serializers.folder.cache.to import serialize_folder_to_cache
from src.folders.infrastructure.storages.cache.base.DAL import FolderDAL


class FolderRepository(IFolderCacheRepository):
    def __init__(self, client: Redis, pipeline: Optional[Redis] = None):
        self.client = client
        self.pipeline = pipeline
        self.folder_dal = FolderDAL(pipeline or client)

    async def cache_by_id(self, id: UUID, entity: FolderResponseInner):
        cache_key = f"folder:{id}"
        cache_data = serialize_folder_to_cache(entity)
        resp = await self.folder_dal.create(cache_key, cache_data)
        return resp

    async def get_by_id(self, id: UUID) -> FolderResponseInner | None:
        cache_key = f"folder:{id}"
        resp = await self.folder_dal.get(cache_key)
        if resp:
            return deserialize_folder_from_cache(resp)
        return None

    async def delete_by_id(self, id: UUID):
        cache_key = f"folder:{id}"
        await self.folder_dal.delete(cache_key)
