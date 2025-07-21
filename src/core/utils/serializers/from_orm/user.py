from src.core.domain.schemas.dataclasses.user import UserResponseInner
from src.core.utils.serializers.from_orm.link import serialize_to_inner_link
from src.infrastructure.storages.db.dal.models import User


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
        links=[serialize_to_inner_link(link) for link in user.links],
    )
