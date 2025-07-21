import datetime
import json
from dataclasses import asdict
from dataclasses import is_dataclass
from typing import Any
from uuid import UUID

from pydantic import EmailStr

from src.core.domain.schemas.dataclasses.user import UserResponseInner


def serialize_user_to_cache(user: UserResponseInner) -> str:
    data = asdict(user)
    data["user_id"] = str(data["user_id"])
    return json.dumps(data, default=_deep_encoder)


def _deep_encoder(obj: Any):
    if isinstance(obj, (UUID, datetime, EmailStr)):
        return str(obj)
    if is_dataclass(obj):
        return asdict(obj)
    if isinstance(obj, set):
        return list(obj)
    raise TypeError(f"Type {type(obj)} is not JSON serializable")
