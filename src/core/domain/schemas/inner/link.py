from uuid import UUID

from core.domain.schemas.base import TunedModel
from pydantic import constr
from pydantic import HttpUrl


class CreateLinkInner(TunedModel):
    user_id: UUID
    name: constr(max_length=20)
    entry_link: str
    short_link: str


class LinkResponseInner(TunedModel):
    link_id: UUID
    user_id: UUID
    name: constr(max_length=20)
    entry_link: HttpUrl
    short_link: str
    clicks: int
