from dataclasses import dataclass

import pytest

from src.core.utils.serializers.to_dict import serialize_to_dict_exclude_none


def test_serialize_to_dict_success(fake_users):
    serialized_dict = serialize_to_dict_exclude_none(fake_users.inner_resp)
    assert serialized_dict["user_id"] == fake_users.inner_resp.user_id
    assert serialized_dict["name"] == fake_users.inner_resp.name
    assert serialized_dict["email"] == fake_users.inner_resp.email
    assert serialized_dict["hashed_password"] == fake_users.inner_resp.hashed_password
    assert serialized_dict["links"] == fake_users.inner_resp.links


def test_serialize_to_dict_exclude_none_success():
    @dataclass
    class Model:
        name: str | None
        email: str | None

    resource = Model(name=None, email="email@mail.com")
    serialized_dict = serialize_to_dict_exclude_none(resource)
    assert serialized_dict["email"] == resource.email
    with pytest.raises(KeyError):
        assert serialized_dict["name"]
