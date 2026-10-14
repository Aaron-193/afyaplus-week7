"""Model adapters. Mock mode is deterministic and makes the capstone runnable offline."""
import re
from typing import Any
from api.config import settings

DISCLAIMER = (
    "Educational demo only; not a diagnosis or treatment plan. "
    "Seek a qualified clinician for medical advice."
)

def estimate_tokens(text: str) -> int:
    # A rough accounting proxy, not an exact tokenizer. Live mode uses provider usage.
    return max(1, (len(text) + 3) // 4)

def mock_triage(case: dict[str, Any], compact: bool) -> dict[str, Any]:
    symptoms = case["symptoms"].lower()
    # Deliberately conservative keywords for a teaching demo, not a validated clinical rule.
    emergency_terms = ("chest pain", "difficulty breathing", "can't breathe", "severe bleeding", "unconscious")
    urgent_terms = ("high fever", "worsening pain", "dehydration", "persistent vomiting")
    if any(term in symptoms for term in emergency_terms):
        urgency = "emergency"
        guidance = "Seek emergency medical care now. Do not rely on this demo for assessment."
    elif any(term in symptoms for term in urgent_terms):
        urgency = "urgent"
        guidance = "Arrange prompt assessment by a qualified healthcare professional."
    else:
        urgency = "routine"
        guidance = "Consider contacting a qualified clinician, especially if symptoms persist or worsen."
    if compact:
        guidance = guidance[:150]
    prompt = f"Age: {case['age']}. Symptoms: {case['symptoms']}"
    return {
        "case_id": case["case_id"], "urgency": urgency, "guidance": guidance,
        "disclaimer": DISCLAIMER, "provider": "mock", "cached": False,
        "input_tokens": estimate_tokens(prompt),
        "output_tokens": estimate_tokens(guidance + DISCLAIMER),
        "estimated_model_cost_usd": 0.0,
    }

def openai_triage(case: dict[str, Any], compact: bool) -> dict[str, Any]:
    # Imported lazily so mock mode works even if the optional SDK is unavailable.
    from openai import OpenAI
    client = OpenAI(api_key=settings.openai_api_key)
    output_cap = settings.compact_output_tokens if compact else settings.max_output_tokens
    response = client.responses.create(
        model=settings.openai_model,
        instructions=(
            "You provide cautious, general health navigation only. Do not diagnose, prescribe, "
            "or claim certainty. If the input suggests a possible emergency, advise emergency care. "
            "Keep the answer concise and include that this is not a diagnosis."
        ),
        input=f"Age: {case['age']}\nSymptoms: {case['symptoms']}",
        max_output_tokens=output_cap,
    )
    usage = getattr(response, "usage", None)
    input_tokens = getattr(usage, "input_tokens", None) or estimate_tokens(case["symptoms"])
    output_tokens = getattr(usage, "output_tokens", None) or estimate_tokens(response.output_text)
    cost = (
        input_tokens * settings.model_input_usd_per_million
        + output_tokens * settings.model_output_usd_per_million
    ) / 1_000_000
    # Keep structured fields stable even though the provider returns natural language.
    text = response.output_text.strip()
    lower = text.lower()
    urgency = "emergency" if any(x in lower for x in ("emergency", "call emergency")) else "routine"
    return {
        "case_id": case["case_id"], "urgency": urgency, "guidance": text,
        "disclaimer": DISCLAIMER, "provider": f"openai:{settings.openai_model}",
        "cached": False, "input_tokens": int(input_tokens), "output_tokens": int(output_tokens),
        "estimated_model_cost_usd": round(cost, 10),
    }

def generate_triage(case: dict[str, Any], compact: bool) -> dict[str, Any]:
    if settings.model_provider == "openai":
        return openai_triage(case, compact)
    return mock_triage(case, compact)
