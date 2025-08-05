from uuid import uuid4

from src.links.core.utils.serializers.link.from_orm import serialize_to_inner_link
from src.links.infrastructure.storages.db.base.models import Link


def test_serialize_to_inner_link_success():
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
    serialized_link = serialize_to_inner_link(link)
    assert serialized_link.link_id == link.link_id
    assert serialized_link.user_id == link.user_id
    assert serialized_link.name == link.name
    assert str(serialized_link.original_url) == link.original_url
    assert serialized_link.short_code == link.short_code
    assert serialized_link.clicks == link.clicks


def test_serialize_to_inner_link_success_with_dict():
    link_id = uuid4()
    user_id = uuid4()
    link = {
        "link_id": link_id,
        "user_id": user_id,
        "name": "test",
        "original_url": "https://yt.com/",
        "short_code": "fsdfsaW2",
        "clicks": 1,
        "folder_id": None,
    }
    serialized_link = serialize_to_inner_link(link)
    assert serialized_link.link_id == link["link_id"]
    assert serialized_link.user_id == link["user_id"]
    assert serialized_link.name == link["name"]
    assert str(serialized_link.original_url) == link["original_url"]
    assert serialized_link.short_code == link["short_code"]
    assert serialized_link.clicks == link["clicks"]
    assert serialized_link.folder_id == link["folder_id"]


def test_serialize_to_inner_link_none():
    link = None
    serialized_link = serialize_to_inner_link(link)
    assert serialized_link is None
