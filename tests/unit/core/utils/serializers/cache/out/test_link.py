import json

from src.core.utils.serializers.cache.out.link import deserialize_link_from_cache


def test_deserialize_link_from_cache_success(fake_links):
    deserialized_link = deserialize_link_from_cache(fake_links.cache)
    fake_loaded_cache = json.loads(fake_links.cache)
    assert str(deserialized_link.link_id) == fake_loaded_cache["link_id"]
    assert deserialized_link.name == fake_loaded_cache["name"]
    assert deserialized_link.original_url == fake_loaded_cache["original_url"]
    assert deserialized_link.clicks == fake_loaded_cache["clicks"]
