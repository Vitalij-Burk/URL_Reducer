from abc import abstractmethod

from src.core.domain.schemas.inner.link import LinkResponseInner
from src.core.ports.cache_repository import ICacheRepository


class ILinkCacheRepository(ICacheRepository[LinkResponseInner]):
    @abstractmethod
    async def cache_by_reduced(self, reduced: str, entity: LinkResponseInner): ...

    @abstractmethod
    async def get_by_reduced(self, reduced: str): ...

    @abstractmethod
    async def delete_by_reduced(self, reduced: str): ...
