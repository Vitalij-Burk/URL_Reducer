from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.core.domain.settings import Config


@dataclass
class CreateLinkInner:
    user_id: UUID
    name: str
    original_url: str
    short_code: str


@dataclass
class LinkResponseInner:
    link_id: UUID
    user_id: UUID
    name: str
    original_url: str
    short_code: str
    clicks: int

    @property
    def short_url(self) -> str:
        return f"{Config.BASE_URL}/{self.short_code}"


@dataclass
class UpdateLinkRequestInner:
    name: Optional[str] = None
    clicks: Optional[int] = None


@dataclass
class DeletedLinkResponseInner:
    deleted_link_id: UUID
