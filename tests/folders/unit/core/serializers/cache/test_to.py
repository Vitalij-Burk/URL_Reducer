import json

from src.folders.core.utils.serializers.folder.cache.to import serialize_folder_to_cache


def test_serialize_folder_to_cache(fake_folders):
    serialized_folder = serialize_folder_to_cache(fake_folders.inner_resp)
    serialized_loaded_folder = json.loads(serialized_folder)
    assert (
        str(fake_folders.inner_resp.folder_id) == serialized_loaded_folder["folder_id"]
    )
    assert fake_folders.inner_resp.name == serialized_loaded_folder["name"]
    assert (
        str(fake_folders.inner_resp.folder_id) == serialized_loaded_folder["folder_id"]
    )
    assert (
        str(fake_folders.inner_resp.parent_id)
        if fake_folders.inner_resp.parent_id
        else None == serialized_loaded_folder["parent_id"]
    )
    assert str(fake_folders.inner_resp.user_id) == serialized_loaded_folder["user_id"]
    assert (
        fake_folders.inner_resp.children_ids == serialized_loaded_folder["children_ids"]
    )
    assert fake_folders.inner_resp.link_ids == serialized_loaded_folder["link_ids"]
