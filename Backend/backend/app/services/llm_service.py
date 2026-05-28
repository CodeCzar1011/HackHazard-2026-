from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ProviderUnavailableError
from app.llm.proxy.llm_router import LLMRouter
from app.llm.proxy.response_filter import filter_response
from app.schemas.request_schema import ChatRequest
from app.schemas.response_schema import ChatResponse
from app.services.threat_service import ThreatService


class LLMService:
    """Secure LLM proxy service."""

    def __init__(self, session: AsyncSession, router: LLMRouter | None = None) -> None:
        self.threat_service = ThreatService(session)
        self.router = router or LLMRouter()

    async def chat(self, request: ChatRequest) -> ChatResponse:
        analysis = await self.threat_service.analyze(request)
        if analysis.decision == "block" or not request.forward_if_safe:
            return ChatResponse(analysis=analysis, provider=request.provider, blocked=True)
        try:
            output = await self.router.complete(request)
        except ProviderUnavailableError as exc:
            return ChatResponse(
                analysis=analysis,
                provider=request.provider,
                blocked=True,
                metadata={"provider_error": str(exc)},
            )
        filtered, findings = filter_response(output)
        return ChatResponse(
            analysis=analysis,
            provider=request.provider,
            output=filtered,
            blocked=False,
            metadata={"response_filter_findings": findings},
        )
