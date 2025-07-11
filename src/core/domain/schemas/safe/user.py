from uuid import UUID

from core.domain.schemas.base import TunedModel
from pydantic import EmailStr

from src.core.domain.schemas.safe.link import LinkResponse


class CreateUser(TunedModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(TunedModel):
    user_id: UUID
    name: str
    email: EmailStr
    links: list[LinkResponse] = []
