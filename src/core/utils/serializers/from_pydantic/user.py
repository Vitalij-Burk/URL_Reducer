from src.core.domain.schemas.inner.user import CreateUserInner
from src.core.domain.schemas.inner.user import UserResponseInner
from src.core.domain.schemas.safe.user import CreateUser
from src.core.domain.schemas.safe.user import UserResponse


def pydantic_inner_user_to_safe(user: UserResponseInner | None) -> UserResponse | None:
    if user is None:
        return None
    return UserResponse(
        user_id=user.user_id, name=user.name, email=user.email, links=user.links or []
    )


def pydantic_create_user_to_inner(
    user: CreateUser | None, hashed_password: str
) -> CreateUserInner | None:
    if user is None:
        return None
    return CreateUserInner(
        name=user.name, email=user.email, hashed_password=hashed_password
    )
