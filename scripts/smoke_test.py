"""Exercise the running API using only the Python standard library."""
import json
import urllib.request

BASE = "http://127.0.0.1:8000"

def call(path, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(
        BASE + path, data=data,
        headers={"Content-Type": "application/json"} if data else {},
    )
    with urllib.request.urlopen(req, timeout=5) as response:
        return json.loads(response.read().decode())

if __name__ == "__main__":
    print("health:", call("/health"))
    payload = {"case_id": "smoke-1", "symptoms": "mild cough for two days", "age": 30}
    print("first request:", call("/triage", payload))
    print("second request (should be cached):", call("/triage", payload))
    print("metrics:", call("/metrics"))
