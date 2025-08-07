from typing import Optional
from uuid import UUID

from pydantic import EmailStr
from pydantic import Field
from pydantic import field_validator

from src.core.domain.schemas.pydantic.base import TunedModel
from src.core.domain.settings import Config


class CreateUserRequest(TunedModel):
    name: str = Field(min_length=4, max_length=20)
    email: EmailStr
    password: str = Field(min_length=6, max_length=20)

    @field_validator("name")
    @classmethod
    def strip_name(cls, name: str) -> str:
        return name.strip()

    @field_validator("password")
    @classmethod
    def check_password(cls, passwd: str) -> str:
        password = passwd.strip()
        safety_count = 0

        if any(s.isdigit() for s in password):
            safety_count += 1
        if any(s.islower() for s in password):
            safety_count += 1
        if any(s.isupper() for s in password):
            safety_count += 1
        if any(s in Config.SPEC_CHARS for s in password):
            safety_count += 1
        if len(password) >= 10:
            safety_count += 1

        if safety_count < 4:
            raise ValueError("Your password is too easy. Try to input harder password.")

        return password


class UserResponse(TunedModel):
    user_id: UUID
    name: str
    email: EmailStr
    link_ids: list[UUID] = Field(default_factory=list)
    folder_ids: list[UUID] = Field(default_factory=list)


class UserResponseOut(TunedModel):
    name: str
    email: EmailStr


class UpdateUserRequest(TunedModel):
    name: Optional[str] = Field(min_length=4, max_length=20)

    @field_validator("name")
    @classmethod
    def strip_name(cls, name: str) -> str:
        if name is not None:
            return name.strip()
        return name


class DeletedUserResponse(TunedModel):
    deleted_user_id: UUID
