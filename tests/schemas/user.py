from dataclasses import dataclass

from src.users.core.domain.schemas.inner.user import CreateUserRequestInner
from src.users.core.domain.schemas.inner.user import DeletedUserResponseInner
from src.users.core.domain.schemas.inner.user import UpdateUserRequestInner
from src.users.core.domain.schemas.inner.user import UserResponseInner
from src.users.core.domain.schemas.out.user import CreateUserRequest
from src.users.core.domain.schemas.out.user import DeletedUserResponse
from src.users.core.domain.schemas.out.user import UpdateUserRequest
from src.users.core.domain.schemas.out.user import UserResponse


@dataclass
class FakeUserCollection:
    cache: str

    safe_resp: UserResponse
    inner_resp: UserResponseInner

    safe_del: DeletedUserResponse
    inner_del: DeletedUserResponseInner

    safe_create: CreateUserRequest
    inner_create: CreateUserRequestInner

    safe_update: UpdateUserRequest
    inner_update: UpdateUserRequestInner
