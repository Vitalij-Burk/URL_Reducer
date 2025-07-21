from abc import abstractmethod

from pydantic import EmailStr

from src.core.domain.schemas.dataclasses.user import UserResponseInner
from src.core.interfaces.repositories.cache import ICacheRepository


class IUserCacheRepository(ICacheRepository[UserResponseInner]):
    @abstractmethod
    async def cache_by_email(self, email: EmailStr, entity: UserResponseInner): ...

    @abstractmethod
    async def get_by_email(self, email: EmailStr): ...

    @abstractmethod
    async def delete_by_email(self, email: EmailStr): ...
