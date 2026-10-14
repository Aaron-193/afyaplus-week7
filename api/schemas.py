"""Request/response contracts shared by mock and live providers."""
from pydantic import BaseModel, Field, ConfigDict

class TriageRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    case_id: str = Field(min_length=1, max_length=80)
    symptoms: str = Field(min_length=1, max_length=4000)
    age: int = Field(ge=0, le=120)
    compact: bool = False

class TriageResponse(BaseModel):
    case_id: str
    urgency: str
    guidance: str
    disclaimer: str
    provider: str
    cached: bool = False
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_model_cost_usd: float = 0.0

class BatchRequest(BaseModel):
    cases: list[TriageRequest] = Field(min_length=1, max_length=50)
