# Week 7 — Cost-Optimised AfyaPlus Triage API

A runnable capstone reference implementation for cost-aware AI deployment. It includes a FastAPI API, deterministic no-key fallback, optional OpenAI Responses API adapter, TTL response cache, compact-output lever, reproducible measurement scripts, token-based cost model, Docker Compose, budget configuration examples, architecture memo, and an executive one-pager.

> **Safety boundary:** This is an educational triage demonstration, not a medical device. It does not diagnose, prescribe, or replace a clinician. Do not send real patient data. The included mock model is the default and all example measurements are local simulations—not production benchmarks.

## Quick start (no API key, Docker, Redis, or cloud account)

Requirements: Python 3.11+ (3.12 recommended).

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn api.main:app --reload
```

Open `http://127.0.0.1:8000/docs`. In another terminal:

```bash
python scripts/smoke_test.py
python -m pytest -q
python cost/cost_model.py
python -m levers.cache_hitrate
python -m cost.sensitivity
```

`/health`, `/triage`, `/metrics`, and `/batch/triage` are available. The mock provider makes the whole workflow testable without paid usage.

## Optional OpenAI mode

1. Copy `.env.example` to `.env`; set `MODEL_PROVIDER=openai` and `OPENAI_API_KEY`.
2. Choose a currently available model for your account in `OPENAI_MODEL`.
3. Keep `MAX_OUTPUT_TOKENS` low and test with a tiny fixture first.
4. Start the API again. Do not commit `.env`.

The code uses the OpenAI Python SDK Responses API. Model availability and prices can change; verify the official pricing page linked below before presenting a final live cost. OpenAI mode can incur charges.

## Configuration

| Variable | Default | Meaning |
|---|---|---|
| `MODEL_PROVIDER` | `mock` | `mock` or `openai` |
| `OPENAI_API_KEY` | empty | Required only for OpenAI mode |
| `OPENAI_MODEL` | `gpt-6-luna` | Must be available to your account; verify current pricing/access |
| `CACHE_TTL_SECONDS` | `300` | Cache lifetime |
| `CACHE_MAX_ITEMS` | `1000` | In-process cache capacity |
| `MAX_INPUT_CHARS` | `4000` | Input bound to limit cost/abuse |
| `MAX_OUTPUT_TOKENS` | `180` | Normal mode output cap |
| `COMPACT_OUTPUT_TOKENS` | `80` | Compact lever output cap |
| `MONTHLY_BUDGET_USD` | `5` | Local application warning threshold, not a cloud billing kill switch |

The in-memory cache is per process and is lost on restart. It is suitable for a local capstone, not a multi-replica production service. Use Redis or another shared cache for distributed deployments.

## Endpoints

- `GET /health` — liveness/configuration status; does not call the model.
- `POST /triage` — one fictional case. Set `compact=true` to use the smaller-output path.
- `POST /batch/triage` — processes a bounded list sequentially and returns item-level results.
- `GET /metrics` — process-local request/cache/token/cost counters.
- `POST /metrics/reset` — reset demo counters (protect or remove this endpoint in production).

Example:

```bash
curl -s http://127.0.0.1:8000/triage \
  -H 'Content-Type: application/json' \
  -d '{"case_id":"demo-001","symptoms":"mild cough for two days","age":30,"compact":false}'
```

Cache keys include normalized case input and compact mode. Do not use a response cache for high-stakes personalized decisions without a privacy, freshness, and clinical-safety review. This demo intentionally accepts fictional/non-identifying inputs only.

## Cost model and measurement honesty

Run `python cost/cost_model.py` for baseline and 10× traffic arithmetic. The default token rates are a **dated configurable assumption** based on the official pricing page checked 2026-10-14, not a guarantee that your selected model is available or priced identically. Change `MODEL_INPUT_USD_PER_MILLION` and `MODEL_OUTPUT_USD_PER_MILLION` to the exact current rates before submission. Infrastructure and people/ops are explicit estimates, not quotes.

The measurement script uses repeated deterministic fixtures. Its cache hits are measured by the script; compact-mode token savings are estimated from configured token budgets. No live LLM quality or GPU quantization benchmark is claimed.

## Deploy with Docker Compose

```bash
docker compose -f deploy/docker-compose.cost.yml up --build
```

Then visit `http://localhost:8000/docs`. Compose includes a health check and FinOps labels. A budget notification is not a hard spending cap; provider billing alerts may be delayed and do not necessarily stop workloads.

## Cloud budget evidence

- `deploy/aws_budget.json` is a request-body example for AWS Budgets. Replace account/contact placeholders and submit it using an authorized AWS API/CLI workflow.
- `deploy/azure_budget_triage.json` is a configuration example for Azure Cost Management. Replace the subscription/scope/contact placeholders and validate against your selected scope/API version.
- `deploy/budget_alert_notes.md` explains thresholds and required evidence.

These files are configuration-as-submitted, not proof that a live cloud budget was created.

## Deliverables

1. `cost/cost_model.md` and executable `cost_model.py`
2. `deploy/` Compose and cloud budget examples
3. `levers/` TTL cache and compact-output lever with measurements
4. `memo/api_vs_selfhost.md`
5. `exec/one_pager.pdf` plus editable `exec/one_pager.md`

## Fallbacks declared

- [x] Redis → in-process TTL/LRU cache (single process only)
- [x] GPU quantization → compact-output/token-cap proxy; not quantization evidence
- [x] Paid cloud → local Docker Compose + cloud budget config examples; no live cloud deployment claimed
- [x] OpenAI credits → deterministic mock provider, same response schema
- [x] Load test → repeatable local fixture script; no production traffic claim

## Before submission

- [ ] Run tests and save terminal output/screenshots.
- [ ] Capture one cache MISS then HIT from `/metrics` or script output.
- [ ] Validate live model pricing and update cost assumptions/footnotes.
- [ ] If cloud is used, capture actual budget and alert configuration.
- [ ] Ask a non-author classmate to review the one-pager.
- [ ] Never commit `.env`, API keys, or patient-identifying information.

## Research links (checked 2026-10-14)

- FastAPI release notes: https://fastapi.tiangolo.com/release-notes/
- OpenAI API pricing: https://developers.openai.com/api/docs/pricing
- OpenAI Python SDK on PyPI: https://pypi.org/project/openai/
- Docker Compose environment-variable guidance: https://docs.docker.com/compose/how-tos/environment-variables/best-practices/
- Docker Compose secrets: https://docs.docker.com/compose/how-tos/use-secrets/
- AWS Budgets API: https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_budgets_CreateBudget.html
- Azure Cost Management budgets API: https://learn.microsoft.com/en-us/rest/api/cost-management/budgets/create-or-update
