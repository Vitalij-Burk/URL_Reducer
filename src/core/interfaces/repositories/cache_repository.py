from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import TypeVar
from uuid import UUID


Entity = TypeVar("Entity")


class ICacheRepository(ABC, Generic[Entity]):
    @abstractmethod
    async def cache_by_id(self, id: UUID, entity: Entity): ...

    @abstractmethod
    async def get_by_id(self, id: UUID): ...

    @abstractmethod
    async def delete_by_id(self, id: UUID): ...
