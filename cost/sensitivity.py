"""Print sensitivity to output length and cache hit rate."""
from cost.cost_model import Assumptions, model_cost_per_request

a = Assumptions()
print("output_tokens,cache_hit_rate,effective_model_usd_per_1k")
for output_tokens in (60, 120, 240, 480):
    for hit_rate in (0.0, 0.25, 0.50, 0.75):
        scenario = Assumptions(
            input_tokens=a.input_tokens, output_tokens=output_tokens,
            input_usd_per_million=a.input_usd_per_million,
            output_usd_per_million=a.output_usd_per_million,
        )
        effective = model_cost_per_request(scenario) * (1 - hit_rate) * 1000
        print(f"{output_tokens},{hit_rate:.0%},{effective:.6f}")
