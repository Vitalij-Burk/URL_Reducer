from dataclasses import dataclass

from src.core.domain.schemas.inner.link import LinkResponseInner
from src.core.domain.schemas.safe.link import LinkResponse


@dataclass
class FakeLinkCollection:
    safe: LinkResponse
    inner: LinkResponseInner
