from abc import abstractmethod

from pydantic import EmailStr

from src.users.core.domain.schemas.inner.user import CreateUserRequestInner
from src.users.core.domain.schemas.inner.user import DeletedUserResponseInner
from src.users.core.domain.schemas.inner.user import UpdateUserRequestInner
from src.users.core.domain.schemas.inner.user import UserResponseInner
from src.users.core.interfaces.repositories.db import IRepository


class IUserRepository(
    IRepository[
        CreateUserRequestInner,
        UpdateUserRequestInner,
        DeletedUserResponseInner,
        UserResponseInner,
    ]
):
    @abstractmethod
    async def get_by_email(self, email: EmailStr) -> UserResponseInner | None: ...
