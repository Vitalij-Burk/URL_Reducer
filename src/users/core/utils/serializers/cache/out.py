import json
from uuid import UUID

from src.users.core.domain.schemas.inner.user import UserResponseInner


def deserialize_user_from_cache(user: str) -> UserResponseInner:
    raw = json.loads(user)
    raw["user_id"] = UUID(raw["user_id"])
    return UserResponseInner(**raw)
