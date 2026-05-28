from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ThreatEvent
from app.db.repositories.threat_event_repository import ThreatEventRepository
from app.detection.pipeline.detection_pipeline import DetectionPipeline
from app.schemas.request_schema import AnalyzeRequest
from app.schemas.response_schema import AnalyzeResponse
from app.websocket.connection_manager import manager


class ThreatService:
    """Application service orchestrating analysis, persistence, and realtime alerts."""

    def __init__(self, session: AsyncSession, pipeline: DetectionPipeline | None = None) -> None:
        self.repo = ThreatEventRepository(session)
        self.pipeline = pipeline or DetectionPipeline()

    async def analyze(self, request: AnalyzeRequest) -> AnalyzeResponse:
        result = await self.pipeline.analyze(request)
        event = ThreatEvent(
            session_id=request.session_id,
            provider=request.provider,
            prompt=request.prompt,
            decision=result.decision,
            risk_score=result.risk_score,
            category=result.category,
            reasons=result.reasons,
            signals={signal.name: signal.model_dump() for signal in result.signals},
        )
        await self.repo.create(event)
        await manager.broadcast(
            {
                "type": f"threat.{result.decision}ed" if result.decision != "allow" else "threat.allowed",
                "payload": result.model_dump(),
            }
        )
        return result

