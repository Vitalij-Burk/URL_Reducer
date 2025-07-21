from abc import abstractmethod

from src.core.domain.schemas.dataclasses.link import CreateLinkInner
from src.core.domain.schemas.dataclasses.link import DeletedLinkResponseInner
from src.core.domain.schemas.dataclasses.link import LinkResponseInner
from src.core.domain.schemas.dataclasses.link import UpdateLinkRequestInner
from src.core.interfaces.repositories.db import IRepository


class ILinkRepository(
    IRepository[
        CreateLinkInner,
        UpdateLinkRequestInner,
        DeletedLinkResponseInner,
        LinkResponseInner,
    ]
):
    @abstractmethod
    async def get_by_short_code(self, short_code: str) -> LinkResponseInner | None: ...
