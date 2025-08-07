import json
from uuid import UUID

from src.users.core.domain.schemas.inner.user import UserResponseInner


def deserialize_user_from_cache(user: str) -> UserResponseInner:
    raw = json.loads(user)
    raw["user_id"] = UUID(raw["user_id"])
    raw["link_ids"] = [UUID(link_id) for link_id in raw["link_ids"]]
    raw["folder_ids"] = [UUID(folder_id) for folder_id in raw["folder_ids"]]
    return UserResponseInner(**raw)
