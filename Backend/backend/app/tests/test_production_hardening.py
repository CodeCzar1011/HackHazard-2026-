from __future__ import annotations

import pytest
import asyncio

from app.core.config import Settings, reload_settings
from app.core.exceptions import ProviderUnavailableError
from app.llm.proxy.llm_router import LLMRouter
from app.schemas.request_schema import ChatRequest


def test_production_rejects_demo_defaults() -> None:
    with pytest.raises(ValueError) as exc:
        Settings(APP_ENV="prod")

    message = str(exc.value)
    assert "DATABASE_URL must use PostgreSQL" in message
    assert "DASHBOARD_API_KEY is required" in message
    assert "REDIS_URL is required" in message
    assert "USE_HASH_EMBEDDINGS_FALLBACK must be false" in message


def test_production_accepts_hardened_config() -> None:
    settings = Settings(
        APP_ENV="prod",
        DATABASE_URL="postgresql+psycopg://user:pass@db:5432/guardaiian",
        AUTO_CREATE_TABLES=False,
        DASHBOARD_API_KEY="secret",
        BACKEND_CORS_ORIGINS=["https://example.com"],
        USE_HASH_EMBEDDINGS_FALLBACK=False,
        ALLOW_IN_MEMORY_VECTOR_FALLBACK=False,
        LOAD_EMBEDDING_MODEL_ON_STARTUP=True,
        REDIS_URL="redis://redis:6379/0",
    )

    assert settings.auth_required is True


def test_openai_router_parses_completion(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    reload_settings()

    async def fake_post_json(self, url: str, json: dict, headers: dict[str, str]) -> dict:
        assert url.endswith("/chat/completions")
        assert headers["Authorization"] == "Bearer test-key"
        return {"choices": [{"message": {"content": "safe answer"}}]}

    monkeypatch.setattr(LLMRouter, "_post_json", fake_post_json)
    output = asyncio.run(
        LLMRouter().complete(ChatRequest(prompt="hello", session_id="s", provider="openai"))
    )

    assert output == "safe answer"


def test_openai_router_fails_closed_without_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    reload_settings()

    with pytest.raises(ProviderUnavailableError):
        asyncio.run(LLMRouter().complete(ChatRequest(prompt="hello", session_id="s", provider="openai")))
