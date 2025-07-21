import json
from uuid import UUID

from src.core.domain.schemas.dataclasses.link import LinkResponseInner


def deserialize_link_from_cache(link: str) -> LinkResponseInner:
    raw = json.loads(link)
    raw["link_id"] = UUID(raw["link_id"])
    raw["user_id"] = UUID(raw["user_id"])
    return LinkResponseInner(**raw)
