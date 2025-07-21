from src.core.domain.schemas.dataclasses.user import DeletedUserResponseInner
from src.core.domain.schemas.dataclasses.user import UserResponseInner
from src.core.domain.schemas.pydantic.user import DeletedUserResponse
from src.core.domain.schemas.pydantic.user import UserResponse
from src.core.utils.serializers.from_inner.link import serialize_to_safe_link


def serialize_to_safe_user(user: UserResponseInner | None) -> UserResponse | None:
    if user is None:
        return None
    links = user.links or []
    return UserResponse(
        user_id=user.user_id,
        name=user.name,
        email=user.email,
        links=[serialize_to_safe_link(link) for link in links],
    )


def serialize_to_safe_deleted_user(
    resp: DeletedUserResponseInner | None,
) -> DeletedUserResponse | None:
    if resp is None:
        return None
    return DeletedUserResponse(deleted_user_id=resp.deleted_user_id)
