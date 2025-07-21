from pydantic import HttpUrl

from src.core.domain.schemas.dataclasses.link import DeletedLinkResponseInner
from src.core.domain.schemas.dataclasses.link import LinkResponseInner
from src.core.domain.schemas.pydantic.link import DeletedLinkResponse
from src.core.domain.schemas.pydantic.link import LinkResponse


def serialize_to_safe_link(link: LinkResponseInner | None) -> LinkResponse:
    if link is None:
        return None
    return LinkResponse(
        link_id=link.link_id,
        user_id=link.user_id,
        name=link.name,
        original_url=HttpUrl(link.original_url),
        short_url=HttpUrl(link.short_url),
        short_code=link.short_code,
        clicks=link.clicks,
    )


def serialize_to_safe_deleted_link(
    resp: DeletedLinkResponseInner | None,
) -> DeletedLinkResponse | None:
    if resp is None:
        return None
    if isinstance(resp, dict):
        resp = DeletedLinkResponseInner(**resp)
    return DeletedLinkResponse(deleted_link_id=resp.deleted_link_id)
