from __future__ import annotations

import httpx

from app.core.config import settings


class GeminiClient:
    """Minimal Gemini client using the REST API."""

    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY must be configured to use GeminiClient")
        self._client = httpx.AsyncClient(
            base_url="https://generativelanguage.googleapis.com/v1beta",
            timeout=settings.LLM_REQUEST_TIMEOUT_SECONDS,
        )

    async def complete(self, prompt: str) -> str:
        params = {"key": settings.GEMINI_API_KEY}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
        }
        resp = await self._client.post(
            "/models/gemini-1.5-flash:generateContent", params=params, json=payload
        )
        resp.raise_for_status()
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

