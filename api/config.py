"""Centralized environment configuration; safe defaults keep local runs free."""
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    model_provider: str = os.getenv("MODEL_PROVIDER", "mock").strip().lower()
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-6-luna")
    cache_ttl_seconds: int = int(os.getenv("CACHE_TTL_SECONDS", "300"))
    cache_max_items: int = int(os.getenv("CACHE_MAX_ITEMS", "1000"))
    max_input_chars: int = int(os.getenv("MAX_INPUT_CHARS", "4000"))
    max_output_tokens: int = int(os.getenv("MAX_OUTPUT_TOKENS", "180"))
    compact_output_tokens: int = int(os.getenv("COMPACT_OUTPUT_TOKENS", "80"))
    monthly_budget_usd: float = float(os.getenv("MONTHLY_BUDGET_USD", "5"))
    model_input_usd_per_million: float = float(os.getenv("MODEL_INPUT_USD_PER_MILLION", "0.10"))
    model_output_usd_per_million: float = float(os.getenv("MODEL_OUTPUT_USD_PER_MILLION", "0.50"))

settings = Settings()

if settings.model_provider not in {"mock", "openai"}:
    raise ValueError("MODEL_PROVIDER must be 'mock' or 'openai'.")
if settings.model_provider == "openai" and not settings.openai_api_key:
    raise ValueError("OPENAI_API_KEY is required when MODEL_PROVIDER=openai.")
if min(settings.cache_ttl_seconds, settings.cache_max_items, settings.max_input_chars,
       settings.max_output_tokens, settings.compact_output_tokens) < 1:
    raise ValueError("Cache limits and token/input caps must be positive.")
