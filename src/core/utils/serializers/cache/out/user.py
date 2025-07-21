import json
from uuid import UUID

from src.core.domain.schemas.dataclasses.link import LinkResponseInner
from src.core.domain.schemas.dataclasses.user import UserResponseInner


def deserialize_user_from_cache(user: str) -> UserResponseInner:
    raw = json.loads(user)
    raw["user_id"] = UUID(raw["user_id"])
    raw["links"] = [
        LinkResponseInner(**_fix_link_fields(link)) for link in raw.get("links", [])
    ]
    return UserResponseInner(**raw)


def _fix_link_fields(link: dict) -> dict:
    if "link_id" in link:
        link["link_id"] = UUID(link["link_id"])
    if "user_id" in link:
        link["user_id"] = UUID(link["user_id"])
    return link
