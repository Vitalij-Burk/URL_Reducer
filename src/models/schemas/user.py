from typing import Optional
from uuid import UUID

from core.models.schemas.base import TunedModel
from models.schemas.link import ShowLink
from pydantic import BaseModel
from pydantic import EmailStr


class CreateUser(TunedModel):
    name: str
    email: EmailStr
    password: str


class ShowUser(TunedModel):
    user_id: UUID
    name: str
    email: EmailStr
    links: list[ShowLink] = []


class UpdateUserRequest(BaseModel):
    name: Optional[str] = None


class DeletedUserResponse(BaseModel):
    deleted_user_id: UUID
