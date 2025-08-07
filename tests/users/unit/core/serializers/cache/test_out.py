import json

from src.users.core.utils.serializers.cache.out import deserialize_user_from_cache


def test_deserialize_user_from_cache_success(fake_users):
    deserialized_user = deserialize_user_from_cache(fake_users.cache)
    fake_loaded_cache = json.loads(fake_users.cache)
    assert deserialized_user.name == fake_loaded_cache["name"]
    assert deserialized_user.email == fake_loaded_cache["email"]
    assert deserialized_user.user_id == fake_loaded_cache["user_id"]
    assert deserialized_user.hashed_password == fake_loaded_cache["hashed_password"]
    assert type(deserialized_user.link_ids) != type(fake_loaded_cache["link_ids"])
    assert type(deserialized_user.folder_ids) != type(fake_loaded_cache["folder_ids"])
