from uuid import UUID

from src.core.domain.schemas.dataclasses.link import CreateLinkInner
from src.core.domain.schemas.dataclasses.link import UpdateLinkRequestInner
from src.core.domain.schemas.pydantic.link import CreateLink
from src.core.domain.schemas.pydantic.link import UpdateLinkRequest


def serialize_to_create_inner_link(
    link: CreateLink | None, user_id: UUID, short_code
) -> CreateLinkInner | None:
    if link is None:
        return None
    return CreateLinkInner(
        user_id=user_id,
        name=str(link.name),
        original_url=str(link.original_url),
        short_code=short_code,
    )


def serialize_to_update_inner_link(
    update_link_params: UpdateLinkRequest | None,
) -> UpdateLinkRequestInner | None:
    if update_link_params is None:
        return None
    return UpdateLinkRequestInner(
        name=str(update_link_params.name) if update_link_params.name else None
    )
