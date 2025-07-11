from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import TypeVar
from uuid import UUID


Entity = TypeVar("Entity")
CreateDTO = TypeVar("CreateDTO")
UpdateDTO = TypeVar("UpdateDTO")
DeleteDTO = TypeVar("DeleteDTO")
ResponseDTO = TypeVar("ResponseDTO")


class IRepository(ABC, Generic[CreateDTO, UpdateDTO, DeleteDTO, ResponseDTO]):
    @abstractmethod
    async def create(self, entity: CreateDTO) -> ResponseDTO: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> ResponseDTO | None: ...

    @abstractmethod
    async def update(self, id: UUID, update_params: dict) -> ResponseDTO | None: ...

    @abstractmethod
    async def delete(self, id: UUID) -> UUID | None: ...
