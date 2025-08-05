import json
from uuid import UUID

from src.folders.core.domain.schemas.inner.folder import FolderResponseInner


def deserialize_folder_from_cache(folder: str) -> FolderResponseInner:
    raw = json.loads(folder)
    raw["user_id"] = UUID(raw["user_id"])
    raw["folder_id"] = UUID(raw["folder_id"])
    raw["parent_id"] = UUID(raw["parent_id"]) if raw["parent_id"] else None
    return FolderResponseInner(**raw)
