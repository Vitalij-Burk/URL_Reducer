from dataclasses import dataclass

from src.core.domain.schemas.dataclasses.link import CreateLinkInner
from src.core.domain.schemas.dataclasses.link import DeletedLinkResponseInner
from src.core.domain.schemas.dataclasses.link import LinkResponseInner
from src.core.domain.schemas.dataclasses.link import UpdateLinkRequestInner
from src.core.domain.schemas.pydantic.link import CreateLink
from src.core.domain.schemas.pydantic.link import DeletedLinkResponse
from src.core.domain.schemas.pydantic.link import LinkResponse
from src.core.domain.schemas.pydantic.link import UpdateLinkRequest


@dataclass
class FakeLinkCollection:
    cache: str

    safe_resp: LinkResponse
    inner_resp: LinkResponseInner

    safe_del: DeletedLinkResponse
    inner_del: DeletedLinkResponseInner

    safe_create: CreateLink
    inner_create: CreateLinkInner

    safe_update: UpdateLinkRequest
    inner_update: UpdateLinkRequestInner
