from src.links.core.utils.serializers.link.from_safe import serialize_to_create_inner_link
from src.links.core.utils.serializers.link.from_safe import serialize_to_update_inner_link


def test_serialize_to_update_inner_link_success(fake_links):
    serialized_update = serialize_to_update_inner_link(fake_links.safe_update)
    assert serialized_update.name == fake_links.safe_update.name


def test_serialize_to_update_inner_link_none():
    serialized_update = serialize_to_update_inner_link(None)
    assert serialized_update is None


def test_serialize_to_create_inner_link_success(fake_links):
    serialized_create = serialize_to_create_inner_link(
        fake_links.safe_create,
        fake_links.inner_create.user_id,
        fake_links.inner_create.short_code,
    )
    assert serialized_create.name == fake_links.safe_create.name
    assert serialized_create.original_url == str(fake_links.safe_create.original_url)


def test_serialize_to_create_inner_link_none():
    serialized_create = serialize_to_create_inner_link(None, None, None)
    assert serialized_create is None
