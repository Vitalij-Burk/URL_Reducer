from src.folders.core.utils.serializers.folder.from_safe import serialize_to_create_inner_folder
from src.folders.core.utils.serializers.folder.from_safe import serialize_to_move_inner_folder
from src.folders.core.utils.serializers.folder.from_safe import serialize_to_update_inner_folder


def test_serialize_to_update_inner_folder_success(fake_folders):
    serialized_update = serialize_to_update_inner_folder(fake_folders.safe_update)
    assert serialized_update.name == fake_folders.safe_update.name


def test_serialize_to_update_inner_folder_none():
    serialized_update = serialize_to_update_inner_folder(None)
    assert serialized_update is None


def test_serialize_to_move_inner_folder_success(fake_folders):
    serialized_update = serialize_to_move_inner_folder(fake_folders.safe_move)
    assert serialized_update.parent_id == fake_folders.safe_move.parent_id


def test_serialize_to_move_inner_folder_none():
    serialized_update = serialize_to_move_inner_folder(None)
    assert serialized_update is None


def test_serialize_to_create_inner_folder_success(fake_folders):
    serialized_create = serialize_to_create_inner_folder(
        fake_folders.safe_create, fake_folders.inner_create.user_id
    )
    assert serialized_create.name == fake_folders.safe_create.name


def test_serialize_to_create_inner_folder_none():
    serialized_create = serialize_to_create_inner_folder(None, None)
    assert serialized_create is None
