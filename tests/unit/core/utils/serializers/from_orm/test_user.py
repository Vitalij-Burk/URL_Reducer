from uuid import uuid4

from src.core.utils.serializers.from_orm.user import serialize_to_inner_user
from src.infrastructure.storages.db.dal.models import User


def test_serialize_to_inner_user_success():
    user_id = uuid4()
    user = User(
        user_id=user_id,
        name="tester",
        email="tester@mail.com",
        hashed_password="fdsafdfdaf",
        links=[],
    )
    serialized_user = serialize_to_inner_user(user)
    assert serialized_user.user_id == user.user_id
    assert serialized_user.name == user.name
    assert serialized_user.email == user.email
    assert serialized_user.links == user.links
    assert serialized_user.hashed_password == user.hashed_password


def test_serialize_to_inner_user_success_with_dict():
    user_id = uuid4()
    user = {
        "user_id": user_id,
        "name": "tester",
        "email": "tester@mail.com",
        "hashed_password": "fdsafdfdaf",
        "links": [],
    }
    serialized_user = serialize_to_inner_user(user)
    assert serialized_user.user_id == user["user_id"]
    assert serialized_user.name == user["name"]
    assert serialized_user.email == user["email"]
    assert serialized_user.links == user["links"]
    assert serialized_user.hashed_password == user["hashed_password"]


def test_serialize_to_inner_user_none():
    user = None
    serialized_user = serialize_to_inner_user(user)
    assert serialized_user is None
