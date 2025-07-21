from src.core.domain.schemas.dataclasses.link import LinkResponseInner
from src.infrastructure.storages.db.dal.models import Link


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
    )
