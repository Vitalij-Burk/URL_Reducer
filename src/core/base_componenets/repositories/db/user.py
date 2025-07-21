from abc import abstractmethod

from pydantic import EmailStr

from src.core.domain.schemas.dataclasses.user import CreateUserInner
from src.core.domain.schemas.dataclasses.user import DeletedUserResponseInner
from src.core.domain.schemas.dataclasses.user import UpdateUserRequestInner
from src.core.domain.schemas.dataclasses.user import UserResponseInner
from src.core.interfaces.repositories.db import IRepository


class IUserRepository(
    IRepository[
        CreateUserInner,
        UpdateUserRequestInner,
        DeletedUserResponseInner,
        UserResponseInner,
    ]
):
    @abstractmethod
    async def get_by_email(self, email: EmailStr) -> UserResponseInner | None: ...
