from typing import Optional
from uuid import UUID

from pydantic import constr
from pydantic import EmailStr
from pydantic import Field

from src.core.domain.schemas.pydantic.base import TunedModel
from src.core.domain.schemas.pydantic.link import LinkResponse


class CreateUser(TunedModel):
    name: constr(max_length=20)
    email: EmailStr
    password: str


class UserResponse(TunedModel):
    user_id: UUID
    name: str
    email: EmailStr
    links: list[LinkResponse] = Field(default_factory=list)


class UpdateUserRequest(TunedModel):
    email: Optional[EmailStr] = None
    name: Optional[constr(max_length=20)] = None


class DeletedUserResponse(TunedModel):
    deleted_user_id: UUID
