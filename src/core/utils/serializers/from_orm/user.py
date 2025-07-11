from src.core.domain.models import User
from src.core.domain.schemas.inner.user import UserResponseInner


def db_user_to_pydantic_inner_user(user: User | None) -> UserResponseInner | None:
    if user is None:
        return None
    return UserResponseInner(
        user_id=user.user_id,
        name=user.name,
        email=user.email,
        hashed_password=user.hashed_password,
        links=user.links or [],
    )
