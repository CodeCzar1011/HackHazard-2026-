from __future__ import annotations

from typing import Any

import httpx

from app.core.config import settings


class OpenAIClient:
    """Minimal OpenAI chat client with sane timeouts and no secret logging."""

    def __init__(self) -> None:
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY must be configured to use OpenAIClient")
        base_url = settings.OPENAI_BASE_URL or "https://api.openai.com/v1"
        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=settings.LLM_REQUEST_TIMEOUT_SECONDS,
        )

    async def complete(self, prompt: str) -> str:
        # Simple, model-agnostic text completion for demo; can be swapped to chat API.
        headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
        payload: dict[str, Any] = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
        }
        resp = await self._client.post("/chat/completions", json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]

