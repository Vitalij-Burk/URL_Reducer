from src.core.utils.serializers.from_safe.user import serialize_to_create_inner_user
from src.core.utils.serializers.from_safe.user import serialize_to_update_inner_user


def test_serialize_to_update_inner_user_success(fake_users):
    serialized_update = serialize_to_update_inner_user(fake_users.safe_update)
    assert serialized_update.name == fake_users.safe_update.name
    assert serialized_update.email == str(fake_users.safe_update.email)


def test_serialize_to_update_inner_user_none():
    serialized_update = serialize_to_update_inner_user(None)
    assert serialized_update is None


def test_serialize_to_create_inner_user_success(fake_users):
    serialized_create = serialize_to_create_inner_user(
        fake_users.safe_create, fake_users.inner_create.hashed_password
    )
    assert serialized_create.name == fake_users.safe_create.name
    assert serialized_create.email == str(fake_users.safe_create.email)


def test_serialize_to_create_inner_user_none():
    serialized_create = serialize_to_create_inner_user(None, None)
    assert serialized_create is None
