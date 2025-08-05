import datetime
import json
from dataclasses import asdict
from dataclasses import is_dataclass
from typing import Any
from uuid import UUID

from pydantic import EmailStr

from src.links.core.domain.schemas.inner.link import LinkResponseInner


def serialize_link_to_cache(link: LinkResponseInner) -> str:
    data = asdict(link)
    data["user_id"] = str(data["user_id"])
    data["link_id"] = str(data["link_id"])
    return json.dumps(data, default=_deep_encoder)


def _deep_encoder(obj: Any):
    if isinstance(obj, (UUID, datetime, EmailStr)):
        return str(obj)
    if is_dataclass(obj):
        return asdict(obj)
    if isinstance(obj, set):
        return list(obj)
    raise TypeError(f"Type {type(obj)} is not JSON serializable")
