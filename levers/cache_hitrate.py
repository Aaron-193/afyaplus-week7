"""Repeat a small fixed fixture to report measured cache hits and estimated savings."""
import json
from api.cache import TTLCache
from api.providers import mock_triage
from levers.cache_triage import cached_call

FIXTURES = [
    {"case_id": "fixture-1", "symptoms": "mild cough for two days", "age": 30},
    {"case_id": "fixture-2", "symptoms": "chest pain and difficulty breathing", "age": 51},
    {"case_id": "fixture-3", "symptoms": "high fever and persistent vomiting", "age": 9},
]

def run(repeats: int = 10):
    cache = TTLCache(ttl_seconds=300, max_items=100)
    model_calls = 0
    estimated_cost = 0.0
    for _ in range(repeats):
        for fixture in FIXTURES:
            key = json.dumps(fixture, sort_keys=True)
            def compute(f=fixture):
                nonlocal model_calls, estimated_cost
                model_calls += 1
                result = mock_triage(f, compact=False)
                estimated_cost += result["estimated_model_cost_usd"]
                return result
            cached_call(cache, key, compute)
    total = repeats * len(FIXTURES)
    return {
        "fixture_requests": total,
        "model_calls_after_cache": model_calls,
        "cache_hits": cache.hits,
        "cache_misses": cache.misses,
        "cache_hit_rate": round(cache.hit_rate, 4),
        "model_calls_avoided": total - model_calls,
        "provider_cost_in_mock_mode_usd": round(estimated_cost, 8),
        "note": "Cache hit rate is measured on deterministic local fixtures; provider cost is zero in mock mode.",
    }

if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
