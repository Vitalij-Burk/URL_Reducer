from uuid import UUID

from src.folders.core.domain.schemas.inner.folder import CreateFolderRequestInner
from src.folders.core.domain.schemas.inner.folder import MoveFolderRequestInner
from src.folders.core.domain.schemas.inner.folder import UpdateFolderRequestInner
from src.folders.core.domain.schemas.out.folder import CreateFolderRequest
from src.folders.core.domain.schemas.out.folder import MoveFolderRequest
from src.folders.core.domain.schemas.out.folder import UpdateFolderRequest


def serialize_to_create_inner_folder(
    folder: CreateFolderRequest | None, user_id: UUID
) -> CreateFolderRequestInner | None:
    if folder is None:
        return None
    return CreateFolderRequestInner(
        user_id=user_id,
        name=str(folder.name),
        parent_id=folder.parent_id if folder.parent_id else None,
    )


def serialize_to_update_inner_folder(
    update_folder_params: UpdateFolderRequest | None,
) -> UpdateFolderRequestInner | None:
    if update_folder_params is None:
        return None
    return UpdateFolderRequestInner(
        name=str(update_folder_params.name) if update_folder_params.name else None,
    )


def serialize_to_move_inner_folder(
    move_folder_params: MoveFolderRequest | None,
) -> MoveFolderRequestInner | None:
    if move_folder_params is None:
        return None
    return MoveFolderRequestInner(
        parent_id=move_folder_params.parent_id,
    )
