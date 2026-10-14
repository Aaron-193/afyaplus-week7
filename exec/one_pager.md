# AfyaPlus AI Triage — Cost-Controlled Pilot Decision

## Recommendation: GO for a limited technical pilot; NO-GO for clinical use

**Unit cost:** Under the stated assumptions, token charges are about **$0.105 per 1,000 uncached requests**. Including estimated infrastructure and operations allocation, the baseline is **$5.905 per 1,000** at 10,000 requests/month. At a 10× volume scenario, fixed-cost allocation falls on paper, but actual capacity costs may rise.

## What we changed

- **Exact-response cache:** In a fixed fixture of 30 requests (three cases repeated ten times), 27 were cache hits: 90% hit rate and 27 model calls avoided. Real traffic may have a lower hit rate.
- **Compact response path:** Reduces the output-token ceiling from 180 to 80 (55.6% lower ceiling). This is a proxy, not quantization; quality and actual token use still need evaluation.

## 10× traffic plan

Bound request size and output tokens; cache exact repeats; monitor latency, errors, token usage and spend; add API replicas only after load tests; use provider rate limits and a documented degraded-mode response. Run local load tests before any live traffic. Budget alerts are warnings, not guaranteed shutdowns.

## Main risk and mitigation

**Risk:** Cached or shortened health guidance may be stale, incomplete, or misleading. **Mitigation:** This remains an educational demo using fictional inputs; do not use for clinical decisions. Require clinician-led validation, privacy review, auditability and a tested fallback before any real use.

## Decision conditions

Proceed only with a $5 monthly budget alert, spending dashboard, bounded token/input settings, secrets excluded from source control, and an owner for alert response. Reassess API vs self-host only when measured sustained volume and credible capacity quotes support a break-even analysis.

*Assumptions: 450 input tokens + 120 output tokens/request; $0.10/M input and $0.50/M output (official price snapshot checked 2026-10-14; re-verify before submission); $18/month infrastructure; 2 operations hours/month at $20/hour; 10,000 baseline requests/month. Cloud costs and staffing are estimates, not vendor quotes. Mock fixture measurements are not production benchmarks.*
