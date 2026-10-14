"""Reusable cache wrapper for measuring repeated identical triage requests."""
from typing import Callable, Any
from api.cache import TTLCache

def cached_call(cache: TTLCache, key: str, compute: Callable[[], dict[str, Any]]) -> dict[str, Any]:
    value = cache.get(key)
    if value is not None:
        value["cached"] = True
        return value
    value = compute()
    value["cached"] = False
    cache.set(key, value)
    return value
