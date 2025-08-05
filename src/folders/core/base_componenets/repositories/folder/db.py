from abc import abstractmethod

from src.folders.core.domain.schemas.inner.folder import CreateFolderRequestInner
from src.folders.core.domain.schemas.inner.folder import DeletedFolderResponseInner
from src.folders.core.domain.schemas.inner.folder import FolderResponseInner
from src.folders.core.domain.schemas.inner.folder import MoveFolderRequestInner
from src.folders.core.domain.schemas.inner.folder import UpdateFolderRequestInner
from src.folders.core.interfaces.repositories.db import IRepository


class IFolderRepository(
    IRepository[
        CreateFolderRequestInner,
        UpdateFolderRequestInner,
        MoveFolderRequestInner,
        DeletedFolderResponseInner,
        FolderResponseInner,
    ]
):
    pass
