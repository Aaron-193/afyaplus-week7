# Optimisation measurements

## Lever 1 — exact-response TTL cache

Fixture: three deterministic fictional cases repeated 10 times (30 total requests), TTL 300 seconds, cache capacity 100.

Run: `python levers/cache_hitrate.py`

Expected mechanics: first pass creates three misses; subsequent 27 requests hit the cache. This yields a measured **90% hit rate** for this intentionally repetitive fixture and avoids 27 model calls. It is not a claim about real traffic; real hit rate depends on repeated identical requests and cache-key privacy/freshness constraints.

## Lever 2 — compact-output token cap

Normal path uses `MAX_OUTPUT_TOKENS=180`; compact path uses `COMPACT_OUTPUT_TOKENS=80`. This is a configuration proxy for a smaller/cheaper response path, **not quantization**. The maximum output budget is 55.6% lower (80 vs 180). Actual token reduction, latency, and quality must be measured against representative prompts and model outputs; a token ceiling does not guarantee a proportional reduction.

| Metric | Baseline | Optimised | Evidence type |
|---|---:|---:|---|
| Cache fixture hit rate | 0% (cache disabled) | 90% | Measured deterministic fixture |
| Model calls for 30 repeated fixture requests | 30 | 3 | Measured deterministic fixture |
| Output token ceiling | 180 | 80 | Configured limit |
| Output ceiling reduction | — | 55.6% | Arithmetic |
| Clinical answer quality | Not clinically validated | Not clinically validated | Must not infer equivalence |

## Trade-offs

- Cache returns an earlier response for an identical request. It can be stale or inappropriate for time-sensitive clinical context; TTL is short, keys are exact, and real patient data must not be used in this demo.
- Compact responses can omit useful context or caveats. Preserve emergency escalation language and run expert-reviewed quality evaluation before any real use.
- Metrics are process-local; multiple containers do not share cache or counters.
