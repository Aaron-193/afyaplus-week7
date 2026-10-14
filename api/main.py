"""HTTP API. Keep handlers small; business rules live in providers/cache modules."""
import hashlib
import json
import logging
import time
from fastapi import FastAPI, HTTPException
from api.cache import TTLCache
from api.config import settings
from api.schemas import TriageRequest, TriageResponse, BatchRequest
from api.providers import generate_triage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("afyaplus")

app = FastAPI(
    title="AfyaPlus Cost-Optimised Triage Demo",
    version="1.0.0",
    description="Educational API; not for clinical use. Use fictional cases only.",
)
cache = TTLCache(settings.cache_ttl_seconds, settings.cache_max_items)
stats = {"requests": 0, "model_calls": 0, "estimated_model_cost_usd": 0.0, "latency_ms": []}

def _cache_key(payload: dict) -> str:
    # Hash rather than log raw symptoms; this is not a replacement for a privacy review.
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()

def _run_case(request: TriageRequest) -> dict:
    if len(request.symptoms) > settings.max_input_chars:
        raise HTTPException(status_code=413, detail="Input exceeds configured MAX_INPUT_CHARS.")
    payload = request.model_dump()
    key = _cache_key(payload)
    cached = cache.get(key)
    if cached is not None:
        cached["cached"] = True
        return cached

    start = time.perf_counter()
    result = generate_triage(payload, request.compact)
    elapsed_ms = (time.perf_counter() - start) * 1000
    stats["model_calls"] += 1
    stats["estimated_model_cost_usd"] += result["estimated_model_cost_usd"]
    stats["latency_ms"].append(elapsed_ms)
    # Prevent unbounded metrics growth during demos.
    stats["latency_ms"] = stats["latency_ms"][-5000:]
    cache.set(key, result)
    return result

@app.get("/health")
def health():
    return {
        "status": "ok",
        "provider": settings.model_provider,
        "cache": "process-local TTL/LRU",
        "monthly_budget_usd": settings.monthly_budget_usd,
    }

@app.post("/triage", response_model=TriageResponse)
def triage(request: TriageRequest):
    stats["requests"] += 1
    return _run_case(request)

@app.post("/batch/triage")
def batch_triage(request: BatchRequest):
    # Bounded synchronous batch path: useful for fixture runs; not a durable async queue.
    results = []
    for case in request.cases:
        stats["requests"] += 1
        try:
            results.append(_run_case(case))
        except HTTPException as exc:
            results.append({"case_id": case.case_id, "error": exc.detail, "status_code": exc.status_code})
    return {"count": len(results), "results": results}

@app.get("/metrics")
def metrics():
    total_cache_checks = cache.hits + cache.misses
    latencies = sorted(stats["latency_ms"])
    p95 = latencies[min(len(latencies) - 1, int(len(latencies) * 0.95))] if latencies else 0.0
    return {
        "requests": stats["requests"],
        "model_calls": stats["model_calls"],
        "cache_hits": cache.hits,
        "cache_misses": cache.misses,
        "cache_hit_rate": round(cache.hit_rate, 4),
        "cache_evictions": cache.evictions,
        "cache_checks": total_cache_checks,
        "estimated_model_cost_usd": round(stats["estimated_model_cost_usd"], 8),
        "p95_model_latency_ms": round(p95, 2),
        "monthly_budget_usd": settings.monthly_budget_usd,
        "budget_warning": stats["estimated_model_cost_usd"] >= settings.monthly_budget_usd,
        "note": "Process-local demo metrics; cost excludes infra/people and may be zero in mock mode.",
    }

@app.post("/metrics/reset")
def reset_metrics():
    # Convenience for repeatable local experiments; protect/remove in a real deployment.
    stats.update(requests=0, model_calls=0, estimated_model_cost_usd=0.0, latency_ms=[])
    cache.clear()
    return {"status": "reset"}
