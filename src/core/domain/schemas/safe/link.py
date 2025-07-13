from uuid import UUID

from core.domain.schemas.base import TunedModel
from pydantic import constr
from pydantic import HttpUrl


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
