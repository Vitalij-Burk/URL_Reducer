from src.users.core.domain.schemas.inner.user import DeletedUserResponseInner
from src.users.core.domain.schemas.inner.user import UserResponseInner
from src.users.core.domain.schemas.out.user import DeletedUserResponse
from src.users.core.domain.schemas.out.user import UserResponse


def serialize_to_safe_user(user: UserResponseInner | None) -> UserResponse | None:
    if user is None:
        return None
    return UserResponse(
        user_id=user.user_id,
        name=user.name,
        email=user.email,
        link_ids=[link_id for link_id in user.link_ids],
        folder_ids=[folder_id for folder_id in user.folder_ids],
    )


def serialize_to_safe_deleted_user(
    resp: DeletedUserResponseInner | None,
) -> DeletedUserResponse | None:
    if resp is None:
        return None
    return DeletedUserResponse(deleted_user_id=resp.deleted_user_id)
