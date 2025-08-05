from src.links.core.utils.serializers.link.from_inner import serialize_to_safe_deleted_link
from src.links.core.utils.serializers.link.from_inner import serialize_to_safe_link


def test_serialize_to_safe_link_success(fake_links):
    serialized_link = serialize_to_safe_link(fake_links.inner_resp)
    assert serialized_link.link_id == fake_links.inner_resp.link_id
    assert serialized_link.user_id == fake_links.inner_resp.user_id
    assert serialized_link.name == fake_links.inner_resp.name
    assert str(serialized_link.original_url) == fake_links.inner_resp.original_url
    assert str(serialized_link.short_url) == fake_links.inner_resp.short_url
    assert serialized_link.clicks == fake_links.inner_resp.clicks
    assert serialized_link.folder_id == fake_links.inner_resp.folder_id


def test_serialize_to_safe_link_none():
    serialized_link = serialize_to_safe_link(None)
    assert serialized_link is None


def test_serialize_to_safe_deleted_link_success(fake_links):
    serialized_resp = serialize_to_safe_deleted_link(fake_links.inner_del)
    assert serialized_resp.deleted_link_id == fake_links.inner_del.deleted_link_id


def test_serialize_to_safe_deleted_link_none():
    serialized_resp = serialize_to_safe_deleted_link(None)
    assert serialized_resp is None
