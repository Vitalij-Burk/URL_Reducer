from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Optional
from uuid import UUID

from src.core.domain.schemas.dataclasses.link import LinkResponseInner


@dataclass
class CreateUserInner:
    name: str
    email: str
    hashed_password: str


@dataclass
class UserResponseInner:
    user_id: UUID
    name: str
    email: str
    hashed_password: str
    links: list[LinkResponseInner] = field(default_factory=list)

    # @classmethod
    # def from_dict(cls, data: Any) -> "UserResponseInner":
    #     if isinstance(data, cls):
    #         return data
    #     data = dict(data)
    #     data["links"] = [LinkResponseInner(
    #         **link) if isinstance(link, dict) else link for link in data.get("links", [])]
    #     return cls(**data)


@dataclass
class UpdateUserRequestInner:
    email: Optional[str] = None
    name: Optional[str] = None


@dataclass
class DeletedUserResponseInner:
    deleted_user_id: UUID
