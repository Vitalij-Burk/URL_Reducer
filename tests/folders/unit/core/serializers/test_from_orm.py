from uuid import uuid4

from src.folders.core.utils.serializers.folder.from_orm import serialize_to_inner_folder
from src.folders.infrastructure.storages.db.base.models import Folder


def test_serialize_to_inner_folder_success():
    folder_id = uuid4()
    user_id = uuid4()
    folder = Folder(
        folder_id=folder_id,
        user_id=user_id,
        name="test",
        parent_id=None,
        children=[],
        links=[],
    )
    serialized_folder = serialize_to_inner_folder(folder)
    assert serialized_folder.folder_id == folder.folder_id
    assert serialized_folder.user_id == folder.user_id
    assert serialized_folder.name == folder.name
    assert serialized_folder.parent_id == folder.parent_id


def test_serialize_to_inner_folder_success_with_dict():
    folder_id = uuid4()
    user_id = uuid4()
    folder = {
        "folder_id": folder_id,
        "user_id": user_id,
        "name": "test",
        "parent_id": None,
        "children": [],
        "links": [],
    }
    serialized_folder = serialize_to_inner_folder(folder)
    assert serialized_folder.folder_id == folder["folder_id"]
    assert serialized_folder.user_id == folder["user_id"]
    assert serialized_folder.name == folder["name"]
    assert serialized_folder.folder_id == folder["folder_id"]
    assert serialized_folder.parent_id == folder["parent_id"]


def test_serialize_to_inner_folder_none():
    folder = None
    serialized_folder = serialize_to_inner_folder(folder)
    assert serialized_folder is None
