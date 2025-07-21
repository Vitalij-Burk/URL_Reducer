from abc import abstractmethod

from src.core.domain.schemas.dataclasses.link import LinkResponseInner
from src.core.interfaces.repositories.cache import ICacheRepository


class ILinkCacheRepository(ICacheRepository[LinkResponseInner]):
    @abstractmethod
    async def cache_by_short_code(self, short_code: str, entity: LinkResponseInner): ...

    @abstractmethod
    async def get_by_short_code(self, short_code: str): ...

    @abstractmethod
    async def delete_by_short_code(self, short_code: str): ...
