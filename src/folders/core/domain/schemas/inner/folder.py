from dataclasses import dataclass
from dataclasses import field
from typing import Optional
from uuid import UUID


@dataclass
class CreateFolderRequestInner:
    user_id: UUID
    name: str
    parent_id: Optional[UUID] = None


@dataclass
class FolderResponseInner:
    folder_id: UUID
    user_id: UUID
    name: str
    parent_id: Optional[UUID] = None
    children_ids: list[UUID] = field(default_factory=list)
    link_ids: list[UUID] = field(default_factory=list)


@dataclass
class UpdateFolderRequestInner:
    name: Optional[str] = None


@dataclass
class MoveFolderRequestInner:
    parent_id: Optional[UUID] = None


@dataclass
class DeletedFolderResponseInner:
    deleted_folder_id: UUID
