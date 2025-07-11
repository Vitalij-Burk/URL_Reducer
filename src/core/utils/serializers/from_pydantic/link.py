from uuid import UUID

from src.core.domain.schemas.inner.link import CreateLinkInner
from src.core.domain.schemas.inner.link import LinkResponseInner
from src.core.domain.schemas.safe.link import CreateLink
from src.core.domain.schemas.safe.link import LinkResponse


def pydantic_inner_link_to_safe(link: LinkResponseInner | None) -> LinkResponse:
    if link is None:
        return None
    return LinkResponse(
        link_id=link.link_id,
        user_id=link.user_id,
        name=link.name,
        entry_link=link.entry_link,
        short_link=link.short_link,
        clicks=link.clicks,
    )


def pydantic_create_link_to_inner(
    link: CreateLink | None, user_id: UUID, short_link
) -> CreateLinkInner | None:
    if link is None:
        return None
    return CreateLinkInner(
        user_id=user_id,
        name=link.name,
        entry_link=str(link.entry_link),
        short_link=short_link,
    )
