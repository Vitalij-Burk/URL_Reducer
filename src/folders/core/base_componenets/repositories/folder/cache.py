from abc import abstractmethod

from src.folders.core.domain.schemas.inner.folder import FolderResponseInner
from src.folders.core.interfaces.repositories.cache import ICacheRepository


class IFolderCacheRepository(ICacheRepository[FolderResponseInner]):
    pass
