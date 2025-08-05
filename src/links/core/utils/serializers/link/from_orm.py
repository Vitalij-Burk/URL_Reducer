from src.links.core.domain.schemas.inner.link import LinkResponseInner
from src.links.infrastructure.storages.db.base.models import Link


def serialize_to_inner_link(link: Link | None) -> LinkResponseInner | None:
    if link is None:
        return None
    if isinstance(link, dict):
        link = Link(**link)
    return LinkResponseInner(
        link_id=link.link_id,
        user_id=link.user_id,
        name=link.name,
        original_url=link.original_url,
        short_code=link.short_code,
        clicks=link.clicks,
        folder_id=link.folder_id if link.folder_id else None,
    )
