from dataclasses import dataclass
from dataclasses import field
from typing import Optional
from uuid import UUID


@dataclass
class CreateUserRequestInner:
    name: str
    email: str
    hashed_password: str


@dataclass
class UserResponseInner:
    user_id: UUID
    name: str
    email: str
    hashed_password: str
    link_ids: list[UUID] = field(default_factory=list)
    folder_ids: list[UUID] = field(default_factory=list)


@dataclass
class UpdateUserRequestInner:
    name: Optional[str] = None


@dataclass
class DeletedUserResponseInner:
    deleted_user_id: UUID
