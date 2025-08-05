from abc import abstractmethod

from src.links.core.domain.schemas.inner.link import CreateLinkRequestInner
from src.links.core.domain.schemas.inner.link import DeletedLinkResponseInner
from src.links.core.domain.schemas.inner.link import LinkResponseInner
from src.links.core.domain.schemas.inner.link import UpdateLinkRequestInner
from src.links.core.interfaces.repositories.db import IRepository


class ILinkRepository(
    IRepository[
        CreateLinkRequestInner,
        UpdateLinkRequestInner,
        DeletedLinkResponseInner,
        LinkResponseInner,
    ]
):
    @abstractmethod
    async def get_by_short_code(self, short_code: str) -> LinkResponseInner | None: ...
