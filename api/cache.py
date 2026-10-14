"""Small process-local TTL/LRU cache used when Redis is unavailable."""
from collections import OrderedDict
from dataclasses import dataclass
from time import monotonic
from typing import Any

@dataclass
class CacheEntry:
    expires_at: float
    value: dict[str, Any]

class TTLCache:
    def __init__(self, ttl_seconds: int = 300, max_items: int = 1000):
        self.ttl_seconds = ttl_seconds
        self.max_items = max_items
        self._items: OrderedDict[str, CacheEntry] = OrderedDict()
        self.hits = 0
        self.misses = 0
        self.evictions = 0

    def get(self, key: str):
        entry = self._items.get(key)
        if entry is None:
            self.misses += 1
            return None
        if entry.expires_at <= monotonic():
            del self._items[key]
            self.misses += 1
            return None
        self._items.move_to_end(key)
        self.hits += 1
        return dict(entry.value)

    def set(self, key: str, value: dict[str, Any]):
        self._items[key] = CacheEntry(monotonic() + self.ttl_seconds, dict(value))
        self._items.move_to_end(key)
        while len(self._items) > self.max_items:
            self._items.popitem(last=False)
            self.evictions += 1

    def clear(self):
        self._items.clear()
        self.hits = self.misses = self.evictions = 0

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total else 0.0
