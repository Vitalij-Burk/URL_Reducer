from uuid import uuid4

from src.core.domain.schemas.inner.user import UserResponseInner
from src.core.domain.schemas.safe.user import CreateUser
from src.core.utils.serializers.from_pydantic.user import pydantic_create_user_to_inner
from src.core.utils.serializers.from_pydantic.user import pydantic_inner_user_to_safe


def test_pydantic_inner_user_to_safe_success():
    user_id = uuid4()
    user = UserResponseInner(
        user_id=user_id,
        name="tester",
        email="tester@mail.com",
        hashed_password="fdsafdfdaf",
        links=[],
    )
    serialized_user = pydantic_inner_user_to_safe(user)
    assert serialized_user.user_id == user.user_id
    assert serialized_user.name == user.name
    assert serialized_user.email == user.email
    assert serialized_user.links == user.links


def test_pydantic_inner_user_to_safe_none():
    user = None
    serialized_user = pydantic_inner_user_to_safe(user)
    assert serialized_user is None


def test_pydantic_create_user_to_inner_success():
    user = CreateUser(name="tester", email="tester@mail.com", password="12345")
    serialized_user = pydantic_create_user_to_inner(user, "fdafsfdas23122")
    assert serialized_user.name == user.name
    assert serialized_user.email == user.email
    assert serialized_user.hashed_password != user.password


def test_pydantic_create_user_to_inner_none():
    user = None
    serialized_user = pydantic_create_user_to_inner(user, "fdafsfdas23122")
    assert serialized_user is None
