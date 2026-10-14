"""Reproducible unit economics; all non-token costs are visible assumptions."""
from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Assumptions:
    input_tokens: int = 450
    output_tokens: int = 120
    input_usd_per_million: float = float(os.getenv("MODEL_INPUT_USD_PER_MILLION", "0.10"))
    output_usd_per_million: float = float(os.getenv("MODEL_OUTPUT_USD_PER_MILLION", "0.50"))
    monthly_infra_usd: float = 18.00
    monthly_ops_hours: float = 2.0
    ops_usd_per_hour: float = 20.00
    monthly_requests: int = 10_000
    spike_multiplier: int = 10

def model_cost_per_request(a: Assumptions) -> float:
    return (a.input_tokens * a.input_usd_per_million + a.output_tokens * a.output_usd_per_million) / 1_000_000

def report(a: Assumptions = Assumptions()) -> dict:
    token_cost = model_cost_per_request(a)
    ops_monthly = a.monthly_ops_hours * a.ops_usd_per_hour
    infra_per_request = a.monthly_infra_usd / a.monthly_requests
    ops_per_request = ops_monthly / a.monthly_requests
    baseline_total = token_cost + infra_per_request + ops_per_request
    spike_requests = a.monthly_requests * a.spike_multiplier
    # Same fixed infra/ops allocation is shown separately at spike; actual scaling may raise it.
    spike_total = token_cost + a.monthly_infra_usd / spike_requests + ops_monthly / spike_requests
    return {
        "assumptions": a.__dict__,
        "token_cost_per_request_usd": token_cost,
        "baseline": {
            "requests": a.monthly_requests, "model_usd_per_1k": token_cost * 1000,
            "infra_usd_per_1k": infra_per_request * 1000,
            "ops_usd_per_1k": ops_per_request * 1000,
            "total_usd_per_1k": baseline_total * 1000,
            "total_usd_per_request": baseline_total,
        },
        "spike_10x": {
            "requests": spike_requests, "model_usd_per_1k": token_cost * 1000,
            "infra_usd_per_1k": a.monthly_infra_usd / spike_requests * 1000,
            "ops_usd_per_1k": ops_monthly / spike_requests * 1000,
            "total_usd_per_1k": spike_total * 1000,
            "total_usd_per_request": spike_total,
            "warning": "Illustrative fixed-cost allocation only; real 10x traffic may require more replicas, cache, and operations.",
        },
    }

if __name__ == "__main__":
    import json
    print(json.dumps(report(), indent=2))
