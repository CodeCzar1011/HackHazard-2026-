from __future__ import annotations

import httpx

from app.core.config import settings


class AnthropicClient:
    """Minimal Anthropic Claude client."""

    def __init__(self) -> None:
        if not settings.ANTHROPIC_API_KEY:
            raise RuntimeError("ANTHROPIC_API_KEY must be configured to use AnthropicClient")
        self._client = httpx.AsyncClient(
            base_url="https://api.anthropic.com/v1",
            timeout=settings.LLM_REQUEST_TIMEOUT_SECONDS,
        )

    async def complete(self, prompt: str) -> str:
        headers = {
            "x-api-key": settings.ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
        }
        payload = {
            "model": "claude-3-5-sonnet-latest",
            "max_tokens": 512,
            "messages": [{"role": "user", "content": prompt}],
        }
        resp = await self._client.post("/messages", json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data["content"][0]["text"]

