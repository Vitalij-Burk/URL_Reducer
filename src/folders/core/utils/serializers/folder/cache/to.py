import json
from dataclasses import asdict
from typing import Any
from uuid import UUID

from src.folders.core.domain.schemas.inner.folder import FolderResponseInner


def serialize_folder_to_cache(folder: FolderResponseInner) -> str:
    data = asdict(folder)
    return json.dumps(data, default=_deep_encoder)


def _deep_encoder(obj: Any):
    if isinstance(obj, UUID):
        return str(obj)
    raise TypeError(f"Type {type(obj)} is not JSON serializable")
