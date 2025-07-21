from dataclasses import dataclass

from src.core.domain.schemas.dataclasses.user import CreateUserInner
from src.core.domain.schemas.dataclasses.user import DeletedUserResponseInner
from src.core.domain.schemas.dataclasses.user import UpdateUserRequestInner
from src.core.domain.schemas.dataclasses.user import UserResponseInner
from src.core.domain.schemas.pydantic.user import CreateUser
from src.core.domain.schemas.pydantic.user import DeletedUserResponse
from src.core.domain.schemas.pydantic.user import UpdateUserRequest
from src.core.domain.schemas.pydantic.user import UserResponse


@dataclass
class FakeUserCollection:
    cache: str

    safe_resp: UserResponse
    inner_resp: UserResponseInner

    safe_del: DeletedUserResponse
    inner_del: DeletedUserResponseInner

    safe_create: CreateUser
    inner_create: CreateUserInner

    safe_update: UpdateUserRequest
    inner_update: UpdateUserRequestInner
