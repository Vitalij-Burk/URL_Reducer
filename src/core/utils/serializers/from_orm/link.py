from src.core.domain.models import Link
from src.core.domain.schemas.inner.link import LinkResponseInner


def db_link_to_pydantic_inner_link(link: Link | None) -> LinkResponseInner | None:
    if link is None:
        return None
    return LinkResponseInner(
        link_id=link.link_id,
        user_id=link.user_id,
        name=link.name,
        entry_link=link.entry_link,
        short_link=link.short_link,
        clicks=link.clicks,
    )
