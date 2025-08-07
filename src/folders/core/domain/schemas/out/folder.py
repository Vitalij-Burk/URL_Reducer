from typing import Optional
from uuid import UUID

from pydantic import Field
from pydantic import field_validator

from src.core.domain.schemas.pydantic.base import TunedModel


class CreateFolderRequest(TunedModel):
    name: str = Field(min_length=4, max_length=20)
    parent_id: Optional[UUID] = None

    @field_validator("name")
    @classmethod
    def strip_name(cls, name: str) -> str:
        return name.strip()


class FolderResponse(TunedModel):
    folder_id: UUID
    user_id: UUID
    parent_id: Optional[UUID] = None
    name: str
    children_ids: list[UUID] = Field(default_factory=list)
    link_ids: list[UUID] = Field(default_factory=list)


class UpdateFolderRequest(TunedModel):
    name: Optional[str] = Field(min_length=4, max_length=20, default=None)

    @field_validator("name")
    @classmethod
    def strip_name(cls, name: str) -> str:
        if name is not None:
            return name.strip()
        return name


class MoveFolderRequest(TunedModel):
    parent_id: Optional[UUID] = None


class DeletedFolderResponse(TunedModel):
    deleted_folder_id: UUID
