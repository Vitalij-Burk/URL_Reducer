from typing import Optional
from uuid import UUID

from pydantic import Field
from pydantic import field_validator
from pydantic import HttpUrl

from src.core.domain.schemas.pydantic.base import TunedModel


class CreateLinkRequest(TunedModel):
    name: str = Field(min_length=4, max_length=20)
    original_url: HttpUrl
    folder_id: Optional[UUID] = None

    @field_validator("name")
    @classmethod
    def strip_name(cls, name: str) -> str:
        return name.strip()


class LinkResponse(TunedModel):
    link_id: UUID
    user_id: UUID
    folder_id: Optional[UUID] = None
    name: str = Field(min_length=4, max_length=20)
    original_url: HttpUrl
    short_url: HttpUrl
    short_code: str
    clicks: int

    @field_validator("name")
    @classmethod
    def strip_name(cls, name: str) -> str:
        return name.strip()


class LinkResponseOut(TunedModel):
    name: str
    original_url: HttpUrl
    short_url: HttpUrl
    short_code: str
    clicks: int


class UpdateLinkRequest(TunedModel):
    name: Optional[str] = Field(min_length=4, max_length=20, default=None)

    @field_validator("name")
    @classmethod
    def strip_name(cls, name: str) -> str:
        if name is not None:
            return name.strip()
        return name


class MoveLinkRequest(TunedModel):
    folder_id: Optional[UUID] = None


class DeletedLinkResponse(TunedModel):
    deleted_link_id: UUID
