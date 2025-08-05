from src.users.core.utils.serializers.from_inner import serialize_to_safe_deleted_user
from src.users.core.utils.serializers.from_inner import serialize_to_safe_user


def test_serialize_to_safe_user_success(fake_users):
    serialized_user = serialize_to_safe_user(fake_users.inner_resp)
    assert serialized_user.user_id == fake_users.inner_resp.user_id
    assert serialized_user.name == fake_users.inner_resp.name


def test_serialize_to_safe_user_none():
    serialized_user = serialize_to_safe_user(None)
    assert serialized_user is None


def test_serialize_to_safe_deleted_user_success(fake_users):
    serialized_resp = serialize_to_safe_deleted_user(fake_users.inner_del)
    assert serialized_resp.deleted_user_id == fake_users.inner_del.deleted_user_id


def test_serialize_to_safe_deleted_user_none():
    serialized_resp = serialize_to_safe_deleted_user(None)
    assert serialized_resp is None
