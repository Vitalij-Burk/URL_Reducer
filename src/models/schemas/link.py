from uuid import UUID

from core.models.schemas.base import TunedModel
from pydantic import BaseModel
from pydantic import constr
from pydantic import HttpUrl


class CreateLink(TunedModel):
    name: constr(max_length=20)
    entry_link: HttpUrl


class ShowLink(TunedModel):
    link_id: UUID
    user_id: UUID
    name: constr(max_length=20)
    entry_link: HttpUrl
    short_link: str
    clicks: int


class UpdateLinkRequest(BaseModel):
    name: constr(max_length=20)


class DeletedLinkResponse(BaseModel):
    deleted_link_id: UUID
