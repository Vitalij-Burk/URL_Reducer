import json

from src.core.utils.serializers.cache.to.user import serialize_user_to_cache


def test_serialize_user_to_cache(fake_users):
    serialized_user = serialize_user_to_cache(fake_users.inner_resp)
    serialized_loaded_user = json.loads(serialized_user)
    assert fake_users.inner_resp.name == serialized_loaded_user["name"]
    assert fake_users.inner_resp.email == serialized_loaded_user["email"]
    assert str(fake_users.inner_resp.user_id) == serialized_loaded_user["user_id"]
    assert (
        fake_users.inner_resp.hashed_password
        == serialized_loaded_user["hashed_password"]
    )
    assert fake_users.inner_resp.links == serialized_loaded_user["links"]
