from uuid import UUID

from core.domain.schemas.base import TunedModel
from pydantic import constr
from pydantic import HttpUrl

from src.core.domain.settings import Config


class CreateLinkInner(TunedModel):
    user_id: UUID
    name: constr(max_length=20)
    original_url: str
    short_code: str


class LinkResponseInner(TunedModel):
    link_id: UUID
    user_id: UUID
    name: constr(max_length=20)
    original_url: HttpUrl
    short_code: str
    clicks: int

    @property
    def short_url(self) -> HttpUrl:
        return f"{Config.BASE_URL}/{self.short_code}"
