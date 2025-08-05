from uuid import UUID

from src.links.core.domain.schemas.inner.link import CreateLinkRequestInner
from src.links.core.domain.schemas.inner.link import MoveLinkRequestInner
from src.links.core.domain.schemas.inner.link import UpdateLinkRequestInner
from src.links.core.domain.schemas.out.link import CreateLinkRequest
from src.links.core.domain.schemas.out.link import MoveLinkRequest
from src.links.core.domain.schemas.out.link import UpdateLinkRequest


def serialize_to_create_inner_link(
    link: CreateLinkRequest | None, user_id: UUID, short_code
) -> CreateLinkRequestInner | None:
    if link is None:
        return None
    return CreateLinkRequestInner(
        user_id=user_id,
        name=str(link.name),
        original_url=str(link.original_url),
        short_code=short_code,
        folder_id=link.folder_id if link.folder_id else None,
    )


def serialize_to_update_inner_link(
    update_link_params: UpdateLinkRequest | None,
) -> UpdateLinkRequestInner | None:
    if update_link_params is None:
        return None
    return UpdateLinkRequestInner(
        name=str(update_link_params.name) if update_link_params.name else None,
    )


def serialize_to_move_inner_link(
    move_link_params: MoveLinkRequest | None,
) -> MoveLinkRequestInner | None:
    if move_link_params is None:
        return None
    return MoveLinkRequestInner(
        folder_id=move_link_params.folder_id,
    )
