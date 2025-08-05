from dataclasses import dataclass

from src.links.core.domain.schemas.inner.link import CreateLinkRequestInner
from src.links.core.domain.schemas.inner.link import DeletedLinkResponseInner
from src.links.core.domain.schemas.inner.link import LinkResponseInner
from src.links.core.domain.schemas.inner.link import MoveLinkRequestInner
from src.links.core.domain.schemas.inner.link import UpdateLinkRequestInner
from src.links.core.domain.schemas.out.link import CreateLinkRequest
from src.links.core.domain.schemas.out.link import DeletedLinkResponse
from src.links.core.domain.schemas.out.link import LinkResponse
from src.links.core.domain.schemas.out.link import MoveLinkRequest
from src.links.core.domain.schemas.out.link import UpdateLinkRequest


@dataclass
class FakeLinkCollection:
    cache: str

    safe_resp: LinkResponse
    inner_resp: LinkResponseInner

    safe_del: DeletedLinkResponse
    inner_del: DeletedLinkResponseInner

    safe_create: CreateLinkRequest
    inner_create: CreateLinkRequestInner

    safe_update: UpdateLinkRequest
    inner_update: UpdateLinkRequestInner

    safe_move: MoveLinkRequest
    inner_move: MoveLinkRequestInner
