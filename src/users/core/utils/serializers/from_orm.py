from src.users.core.domain.schemas.inner.user import UserResponseInner
from src.users.infrastructure.storages.db.base.DAL import User


def serialize_to_inner_user(user: User | None) -> UserResponseInner | None:
    if user is None:
        return None
    if isinstance(user, dict):
        user = User(**user)
    return UserResponseInner(
        user_id=user.user_id,
        name=user.name,
        email=user.email,
        hashed_password=user.hashed_password,
        link_ids=[link.link_id for link in user.links],
        folder_ids=[link.folder_id for link in user.folders],
    )
