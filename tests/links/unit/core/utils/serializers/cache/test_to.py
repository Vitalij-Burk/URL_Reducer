import json

from src.links.core.utils.serializers.link.cache.to import serialize_link_to_cache


def test_serialize_link_to_cache(fake_links):
    serialized_link = serialize_link_to_cache(fake_links.inner_resp)
    serialized_loaded_link = json.loads(serialized_link)
    assert str(fake_links.inner_resp.link_id) == serialized_loaded_link["link_id"]
    assert fake_links.inner_resp.name == serialized_loaded_link["name"]
    assert fake_links.inner_resp.original_url == serialized_loaded_link["original_url"]
    assert fake_links.inner_resp.clicks == serialized_loaded_link["clicks"]
    assert str(fake_links.inner_resp.folder_id) == serialized_loaded_link["folder_id"]
