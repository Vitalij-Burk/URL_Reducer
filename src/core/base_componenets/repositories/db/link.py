from abc import abstractmethod

from src.core.domain.schemas.general.link import DeletedLinkResponse
from src.core.domain.schemas.general.link import UpdateLinkRequest
from src.core.domain.schemas.inner.link import CreateLinkInner
from src.core.domain.schemas.inner.link import LinkResponseInner
from src.core.interfaces.repositories.db_repository import IRepository


class ILinkRepository(
    IRepository[
        CreateLinkInner, UpdateLinkRequest, DeletedLinkResponse, LinkResponseInner
    ]
):
    @abstractmethod
    async def get_by_short_code(self, short_code: str) -> LinkResponseInner | None: ...
