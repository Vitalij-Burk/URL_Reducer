from uuid import uuid4

from src.core.utils.serializers.from_orm.link import db_link_to_pydantic_inner_link
from src.infrastructure.storages.db.dal.models import Link


def test_pydantic_inner_link_to_safe_success():
    link_id = uuid4()
    user_id = uuid4()
    link = Link(
        link_id=link_id,
        user_id=user_id,
        name="test",
        original_url="https://yt.com/",
        short_code="fsdfsaW2",
        clicks=1,
    )
    serialized_link = db_link_to_pydantic_inner_link(link)
    assert serialized_link.link_id == link.link_id
    assert serialized_link.user_id == link.user_id
    assert serialized_link.name == link.name
    assert str(serialized_link.original_url) == link.original_url
    assert serialized_link.short_code == link.short_code
    assert serialized_link.clicks == link.clicks


def test_pydantic_inner_link_to_safe_none():
    link = None
    serialized_link = db_link_to_pydantic_inner_link(link)
    assert serialized_link is None
