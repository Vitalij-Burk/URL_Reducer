from uuid import uuid4

from src.core.domain.schemas.inner.link import LinkResponseInner
from src.core.domain.schemas.safe.link import CreateLink
from src.core.utils.serializers.from_pydantic.link import pydantic_create_link_to_inner
from src.core.utils.serializers.from_pydantic.link import pydantic_inner_link_to_safe


def test_pydantic_inner_link_to_safe_success():
    link_id = uuid4()
    user_id = uuid4()
    link = LinkResponseInner(
        link_id=link_id,
        user_id=user_id,
        name="test",
        original_url="https://yt.com",
        short_code="fsdfsaW2",
        clicks=1,
    )
    serialized_link = pydantic_inner_link_to_safe(link)
    assert serialized_link.link_id == link.link_id
    assert serialized_link.user_id == link.user_id
    assert serialized_link.name == link.name
    assert serialized_link.original_url == link.original_url
    assert str(serialized_link.short_url) == link.short_url
    assert serialized_link.clicks == link.clicks


def test_pydantic_inner_link_to_safe_none():
    link = None
    serialized_link = pydantic_inner_link_to_safe(link)
    assert serialized_link is None


def test_pydantic_create_link_to_inner_success():
    user_id = uuid4()
    link = CreateLink(name="tester", original_url="https://yt.com")
    serialized_link = pydantic_create_link_to_inner(link, user_id, "fasdfE12")
    assert serialized_link.name == link.name
    assert serialized_link.original_url == str(link.original_url)
    assert serialized_link.short_code is not None


def test_pydantic_create_link_to_inner_none():
    user_id = uuid4()
    link = None
    serialized_link = pydantic_create_link_to_inner(link, user_id, "fasdfE12")
    assert serialized_link is None
