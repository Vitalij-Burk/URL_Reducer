from src.users.core.domain.schemas.inner.user import CreateUserRequestInner
from src.users.core.domain.schemas.inner.user import UpdateUserRequestInner
from src.users.core.domain.schemas.out.user import CreateUserRequest
from src.users.core.domain.schemas.out.user import UpdateUserRequest


def serialize_to_create_inner_user(
    user: CreateUserRequest | None, hashed_password: str
) -> CreateUserRequestInner | None:
    if user is None:
        return None
    return CreateUserRequestInner(
        name=str(user.name), email=user.email, hashed_password=hashed_password
    )


def serialize_to_update_inner_user(
    update_user_params: UpdateUserRequest | None,
) -> UpdateUserRequestInner | None:
    if update_user_params is None:
        return None
    return UpdateUserRequestInner(
        name=str(update_user_params.name) if update_user_params.name else None,
    )
