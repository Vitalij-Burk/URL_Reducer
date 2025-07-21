from typing import Optional
from uuid import UUID

from pydantic import constr
from pydantic import HttpUrl

from src.core.domain.schemas.pydantic.base import TunedModel


class CreateLink(TunedModel):
    name: constr(max_length=20)
    original_url: HttpUrl


class LinkResponse(TunedModel):
    link_id: UUID
    user_id: UUID
    name: constr(max_length=20)
    original_url: HttpUrl
    short_url: HttpUrl
    short_code: str
    clicks: int


class UpdateLinkRequest(TunedModel):
    name: Optional[constr(max_length=20)] = None


class DeletedLinkResponse(TunedModel):
    deleted_link_id: UUID
