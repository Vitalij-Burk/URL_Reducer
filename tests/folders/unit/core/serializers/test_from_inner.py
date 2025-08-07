from src.folders.core.utils.serializers.folder.from_inner import (
    serialize_to_safe_deleted_folder,
)
from src.folders.core.utils.serializers.folder.from_inner import (
    serialize_to_safe_folder,
)


def test_serialize_to_safe_folder_success(fake_folders):
    serialized_folder = serialize_to_safe_folder(fake_folders.inner_resp)
    assert serialized_folder.folder_id == fake_folders.inner_resp.folder_id
    assert serialized_folder.user_id == fake_folders.inner_resp.user_id
    assert serialized_folder.name == fake_folders.inner_resp.name
    assert serialized_folder.folder_id == fake_folders.inner_resp.folder_id
    assert serialized_folder.parent_id == fake_folders.inner_resp.parent_id
    assert serialized_folder.link_ids == fake_folders.inner_resp.link_ids
    assert serialized_folder.children_ids == fake_folders.inner_resp.children_ids


def test_serialize_to_safe_folder_none():
    serialized_folder = serialize_to_safe_folder(None)
    assert serialized_folder is None


def test_serialize_to_safe_deleted_folder_success(fake_folders):
    serialized_resp = serialize_to_safe_deleted_folder(fake_folders.inner_del)
    assert serialized_resp.deleted_folder_id == fake_folders.inner_del.deleted_folder_id


def test_serialize_to_safe_deleted_folder_none():
    serialized_resp = serialize_to_safe_deleted_folder(None)
    assert serialized_resp is None
