from uuid import UUID

from core.domain.schemas.base import TunedModel
from pydantic import EmailStr

from src.core.domain.schemas.inner.link import LinkResponseInner


class CreateUserInner(TunedModel):
    name: str
    email: EmailStr
    hashed_password: str


class UserResponseInner(TunedModel):
    user_id: UUID
    name: str
    email: EmailStr
    hashed_password: str
    links: list[LinkResponseInner] = []
