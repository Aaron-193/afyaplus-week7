"""Small sequential batch helper; intentionally not presented as a durable queue."""
from api.schemas import TriageRequest
from api.main import _run_case

def process_batch(cases: list[TriageRequest]) -> list[dict]:
    # A real production queue needs persistence, retries, idempotency and back-pressure.
    return [_run_case(case) for case in cases]
