from src.folders.core.domain.schemas.inner.folder import FolderResponseInner
from src.folders.infrastructure.storages.db.base.models import Folder


def serialize_to_inner_folder(
    folder: Folder | None, include_inner_fields: bool = True
) -> FolderResponseInner | None:
    if folder is None:
        return None
    if isinstance(folder, dict):
        folder = Folder(**folder)
    return FolderResponseInner(
        folder_id=folder.folder_id,
        user_id=folder.user_id,
        name=folder.name,
        parent_id=folder.parent_id,
        children_ids=(
            [child.folder_id for child in folder.children]
            if include_inner_fields
            else None
        ),
        link_ids=(
            [link.link_id for link in folder.links] if include_inner_fields else None
        ),
    )
