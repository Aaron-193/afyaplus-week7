from fastapi.testclient import TestClient
from api.main import app, cache, stats

client = TestClient(app)

def setup_function():
    cache.clear()
    stats.update(requests=0, model_calls=0, estimated_model_cost_usd=0.0, latency_ms=[])

def test_health_is_available():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_triage_and_cache_hit():
    payload = {"case_id": "t1", "symptoms": "mild cough for two days", "age": 30}
    first = client.post("/triage", json=payload)
    second = client.post("/triage", json=payload)
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["urgency"] in {"routine", "urgent", "emergency"}
    assert second.json()["cached"] is True
    assert client.get("/metrics").json()["cache_hits"] == 1

def test_emergency_keyword_is_escalated_in_mock_mode():
    # This test exercises the demo heuristic, not clinical correctness.
    from api.providers import mock_triage
    result = mock_triage({"case_id": "e1", "symptoms": "chest pain", "age": 40}, False)
    assert result["urgency"] == "emergency"

def test_extra_fields_rejected():
    response = client.post("/triage", json={
        "case_id": "x", "symptoms": "cough", "age": 30, "unexpected": True
    })
    assert response.status_code == 422

def test_batch_is_bounded_and_returns_results():
    response = client.post("/batch/triage", json={"cases": [
        {"case_id": "b1", "symptoms": "mild cough", "age": 20},
        {"case_id": "b2", "symptoms": "chest pain", "age": 50, "compact": True}
    ]})
    assert response.status_code == 200
    assert response.json()["count"] == 2
