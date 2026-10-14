# Architecture memo: hosted model API vs self-hosted open model

**Decision:** Use a hosted model API for the capstone prototype, behind a provider adapter and strict cost controls. Revisit self-hosting only after representative, sustained volume and quality requirements justify the operational burden.

## Workload and assumptions

The reference workload assumes 10,000 requests/month, 450 input tokens and 120 output tokens per request. The illustrative token price is $0.10 per million input tokens and $0.50 per million output tokens (official price page checked 2026-10-14; verify model/account rates before submitting). This is about $0.105 in model charges per 1,000 uncached requests. Hosting, observability, support, security, model evaluation, and staff time remain separate costs.

A self-hosted model is not “free”: budget for GPU/accelerator or CPU capacity, idle time, redundancy, storage, network, upgrades, security patching, inference serving, monitoring, on-call response, model evaluation, and engineering time. No self-hosted benchmark was run for this capstone, so any break-even estimate is illustrative rather than measured.

## Comparison

| Dimension | Hosted API | Self-hosted open model |
|---|---|---|
| Initial effort | Low; API integration and key controls | High; model selection, serving, deployment, security and evaluation |
| Cost shape | Mostly usage-based; predictable per-token rates if usage is bounded | Mostly capacity + operations; can be attractive at high sustained utilization |
| Scaling | Provider manages model fleet; account rate limits still apply | Team owns autoscaling, queueing, GPU capacity and capacity planning |
| Latency | Network/provider dependent; often strong baseline performance | Can be low within a region, but depends on hardware, batching and model size |
| Data control | Data sent to selected provider under its terms/settings | Greater infrastructure control, but team owns access, logging and retention |
| Quality | Strong managed models and provider updates; model behavior can change | Full model/version control; quality may be lower and tuning/evaluation is team-owned |
| Failure modes | Provider outage, quota, rate limit, price/model changes | Hardware failure, capacity exhaustion, deployment defects, model-server incidents |
| Governance | Vendor and data-processing review required | Infrastructure, model license, patching, security and model governance required |

## Break-even sketch

For a self-hosted option, let monthly fixed cost be `F` (GPU/CPU capacity + operations) and marginal cost per request be `v`. Let hosted API cost per request be `a`. Ignoring quality differences, self-hosting becomes cheaper when:

`F + v × monthly_requests < a × monthly_requests`

If `a > v`, break-even volume is `F / (a - v)`. Example only: assume self-hosting costs $600/month fixed and $0.00002/request variable, while hosted model cost is $0.000105/request. Break-even is approximately `600 / (0.000105 - 0.00002) = 7.06 million requests/month`. This is a deliberately transparent arithmetic scenario, **not a quote or measured benchmark**. It omits potential hosted-model price tiers and differences in quality, staffing, redundancy and accelerator utilization. Replace the inputs with quotes and load-test data before making a purchasing decision.

## What would change the decision?

1. Sustained volume approaches a measured break-even point and utilization stays high enough to amortize capacity.
2. Data residency/control requirements, predictable low latency, or offline operation outweigh extra operational burden.
3. A representative quality and safety evaluation shows an open model meets the workload's needs, and the team can support production inference reliably.

## Recommendation and conditions

Proceed with hosted API for prototype use only, with a $5 monthly budget alert, bounded inputs/output, exact-response cache, rate limits at the edge, usage monitoring, and a mock fallback for development. Do not use this demo for real clinical triage. For a production health workflow, require clinical governance, privacy/security review, evaluation by qualified professionals, incident response, audit controls and an approved fallback before go-live.
