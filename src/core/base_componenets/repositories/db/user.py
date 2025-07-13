from abc import abstractmethod

from pydantic import EmailStr

from src.core.domain.schemas.general.user import DeletedUserResponse
from src.core.domain.schemas.general.user import UpdateUserRequest
from src.core.domain.schemas.inner.user import CreateUserInner
from src.core.domain.schemas.inner.user import UserResponseInner
from src.core.interfaces.repositories.db_repository import IRepository


class IUserRepository(
    IRepository[
        CreateUserInner, UpdateUserRequest, DeletedUserResponse, UserResponseInner
    ]
):
    @abstractmethod
    async def get_by_email(self, email: EmailStr) -> UserResponseInner | None: ...
