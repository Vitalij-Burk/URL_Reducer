from uuid import UUID

from src.folders.core.domain.schemas.inner.folder import DeletedFolderResponseInner
from src.folders.core.domain.schemas.inner.folder import FolderResponseInner
from src.folders.core.domain.schemas.out.folder import DeletedFolderResponse
from src.folders.core.domain.schemas.out.folder import FolderResponse


def serialize_to_safe_folder(
    folder: FolderResponseInner | None, include_inner_fields: bool = True
) -> FolderResponse:
    if folder is None:
        return None
    return FolderResponse(
        folder_id=folder.folder_id,
        name=folder.name,
        parent_id=folder.parent_id if folder.parent_id else None,
        user_id=folder.user_id,
        children_ids=(
            [child_id for child_id in folder.children_ids]
            if include_inner_fields
            else []
        ),
        link_ids=(
            [link_id for link_id in folder.link_ids] if include_inner_fields else []
        ),
    )


def serialize_to_safe_deleted_folder(
    resp: DeletedFolderResponseInner | None,
) -> DeletedFolderResponse | None:
    if resp is None:
        return None
    if isinstance(resp, dict):
        resp = DeletedFolderResponseInner(**resp)
    return DeletedFolderResponse(deleted_folder_id=resp.deleted_folder_id)
