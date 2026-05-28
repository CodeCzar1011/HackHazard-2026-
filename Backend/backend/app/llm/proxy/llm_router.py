from __future__ import annotations

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.exceptions import ProviderUnavailableError
from app.schemas.request_schema import ChatRequest


class LLMRouter:
    """Provider router with bounded network calls and safe failures."""

    async def complete(self, request: ChatRequest) -> str:
        if request.provider == "local":
            return await self._complete_local(request)
        if request.provider == "openai":
            return await self._complete_openai(request)
        if request.provider == "anthropic":
            return await self._complete_anthropic(request)
        if request.provider == "gemini":
            return await self._complete_gemini(request)
        raise ProviderUnavailableError(f"Provider '{request.provider}' is not supported.")

    async def _complete_local(self, request: ChatRequest) -> str:
        if not settings.LOCAL_LLM_ENDPOINT:
            if settings.is_production:
                raise ProviderUnavailableError("LOCAL_LLM_ENDPOINT is required for local provider in production.")
            return (
                "GuardAIian local demo provider: request passed firewall checks. "
                "Configure provider API keys to forward to external LLMs."
            )
        response = await self._post_json(
            settings.LOCAL_LLM_ENDPOINT,
            json={"prompt": request.prompt, "session_id": request.session_id},
            headers={},
        )
        return str(response.get("output") or response.get("text") or response)

    async def _complete_openai(self, request: ChatRequest) -> str:
        if not settings.OPENAI_API_KEY:
            raise ProviderUnavailableError("OPENAI_API_KEY is not configured.")
        base_url = (settings.OPENAI_BASE_URL or "https://api.openai.com/v1").rstrip("/")
        response = await self._post_json(
            f"{base_url}/chat/completions",
            json={
                "model": settings.OPENAI_MODEL,
                "messages": [{"role": "user", "content": request.prompt}],
            },
            headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
        )
        try:
            return str(response["choices"][0]["message"]["content"])
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderUnavailableError("OpenAI returned an unexpected response shape.") from exc

    async def _complete_anthropic(self, request: ChatRequest) -> str:
        if not settings.ANTHROPIC_API_KEY:
            raise ProviderUnavailableError("ANTHROPIC_API_KEY is not configured.")
        response = await self._post_json(
            "https://api.anthropic.com/v1/messages",
            json={
                "model": settings.ANTHROPIC_MODEL,
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": request.prompt}],
            },
            headers={
                "x-api-key": settings.ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
            },
        )
        try:
            content = response["content"][0]
            return str(content.get("text", ""))
        except (KeyError, IndexError, TypeError, AttributeError) as exc:
            raise ProviderUnavailableError("Anthropic returned an unexpected response shape.") from exc

    async def _complete_gemini(self, request: ChatRequest) -> str:
        if not settings.GEMINI_API_KEY:
            raise ProviderUnavailableError("GEMINI_API_KEY is not configured.")
        response = await self._post_json(
            (
                "https://generativelanguage.googleapis.com/v1beta/models/"
                f"{settings.GEMINI_MODEL}:generateContent?key={settings.GEMINI_API_KEY}"
            ),
            json={"contents": [{"parts": [{"text": request.prompt}]}]},
            headers={},
        )
        try:
            return str(response["candidates"][0]["content"]["parts"][0]["text"])
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderUnavailableError("Gemini returned an unexpected response shape.") from exc

    @retry(
        stop=stop_after_attempt(settings.LLM_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=0.25, min=0.25, max=2),
        reraise=True,
    )
    async def _post_json(self, url: str, json: dict, headers: dict[str, str]) -> dict:
        timeout = httpx.Timeout(settings.LLM_REQUEST_TIMEOUT_SECONDS)
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(url, json=json, headers=headers)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as exc:
            raise ProviderUnavailableError(f"Provider request failed: {exc}") from exc
