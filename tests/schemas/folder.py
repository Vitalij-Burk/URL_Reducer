from dataclasses import dataclass

from src.folders.core.domain.schemas.inner.folder import CreateFolderRequestInner
from src.folders.core.domain.schemas.inner.folder import DeletedFolderResponseInner
from src.folders.core.domain.schemas.inner.folder import FolderResponseInner
from src.folders.core.domain.schemas.inner.folder import MoveFolderRequestInner
from src.folders.core.domain.schemas.inner.folder import UpdateFolderRequestInner
from src.folders.core.domain.schemas.out.folder import CreateFolderRequest
from src.folders.core.domain.schemas.out.folder import DeletedFolderResponse
from src.folders.core.domain.schemas.out.folder import FolderResponse
from src.folders.core.domain.schemas.out.folder import MoveFolderRequest
from src.folders.core.domain.schemas.out.folder import UpdateFolderRequest


@dataclass
class FakeFolderCollection:
    cache: str

    safe_resp: FolderResponse
    inner_resp: FolderResponseInner

    safe_del: DeletedFolderResponse
    inner_del: DeletedFolderResponseInner

    safe_create: CreateFolderRequest
    inner_create: CreateFolderRequestInner

    safe_update: UpdateFolderRequest
    inner_update: UpdateFolderRequestInner

    safe_move: MoveFolderRequest
    inner_move: MoveFolderRequestInner
