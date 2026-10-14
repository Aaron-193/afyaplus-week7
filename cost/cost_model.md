# Cost model and unit economics

**Pricing check date:** 2026-10-14. Official OpenAI pricing page is the source of token rates; update the environment variables to match the actual model and account before submission. Default assumption here is **$0.10 / 1M input tokens and $0.50 / 1M output tokens**, corresponding to the listed GPT-6 Luna standard short-context rates at the time checked. Model access and pricing may change. [Source](https://developers.openai.com/api/docs/pricing).

## Explicit assumptions

| Input | Value | Basis |
|---|---:|---|
| Average prompt | 450 tokens/request | Workload assumption; replace with measured usage |
| Average completion | 120 tokens/request | Workload assumption; replace with measured usage |
| Input rate | $0.10 / 1M tokens | Official price snapshot, checked 2026-10-14 |
| Output rate | $0.50 / 1M tokens | Official price snapshot, checked 2026-10-14 |
| Infrastructure | $18/month | Planning estimate, not a cloud quote |
| Operations | 2 hours/month × $20/hour = $40 | Planning assumption, not a salary benchmark |
| Baseline volume | 10,000 requests/month | Scenario assumption |
| Spike | 10× = 100,000 requests/month | Same workload, not a measured traffic event |

Formula:
`model_cost/request = (input_tokens × input_rate + output_tokens × output_rate) / 1,000,000`

Baseline model cost is $0.000105/request or **$0.105 per 1,000**. With the stated fixed infrastructure and people/ops allocation, total baseline is **$5.905 per 1,000**. The 10× scenario reduces fixed-cost allocation per request, but that does **not** mean the infrastructure can actually handle 10× traffic at the same monthly spend; capacity and autoscaling may increase costs.

Run `python cost/cost_model.py` for the generated figures. The calculator is the source of truth if assumptions are changed. Mock mode's actual provider charge is $0; this cost model estimates a live token-billed path. Cache-hit savings are computed by multiplying model cost by `1 - hit_rate`; they do not remove hosting, monitoring, or people costs.

## Limitations

- Token counts above are fixture assumptions; production accounting should use provider-reported usage.
- API prices can vary by model, cached tokens, batch mode, context size, region, and other product features.
- No exchange-rate conversion, taxes, storage, egress, observability vendor, incident response, or clinical validation cost is included.
- A budget alert warns; it is not a guaranteed hard stop.
