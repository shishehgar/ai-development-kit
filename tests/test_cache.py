from aidk.core.cache import Cache


def test_cache_store():

    cache = Cache()

    cache.set("a", 1)

    assert cache.has("a")

    assert cache.get("a") == 1


def test_cache_default():

    cache = Cache()

    assert cache.get("missing") is None

    assert cache.get("missing", 100) == 100


def test_cache_clear():

    cache = Cache()

    cache.set("a", 1)

    cache.clear()

    assert cache.size == 0
