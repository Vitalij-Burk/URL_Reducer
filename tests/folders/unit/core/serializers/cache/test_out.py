import json

from src.folders.core.utils.serializers.folder.cache.out import (
    deserialize_folder_from_cache,
)


def test_deserialize_folder_from_cache_success(fake_folders):
    deserialized_folder = deserialize_folder_from_cache(fake_folders.cache)
    fake_loaded_cache = json.loads(fake_folders.cache)
    assert str(deserialized_folder.folder_id) == fake_loaded_cache["folder_id"]
    assert deserialized_folder.name == fake_loaded_cache["name"]
    assert str(deserialized_folder.folder_id) == fake_loaded_cache["folder_id"]
    assert str(deserialized_folder.user_id) == fake_loaded_cache["user_id"]
    assert deserialized_folder.link_ids == fake_loaded_cache["link_ids"]
    assert deserialized_folder.childred_ids == fake_loaded_cache["childred_ids"]
    assert deserialized_folder.parent_id == fake_loaded_cache["parent_id"]
