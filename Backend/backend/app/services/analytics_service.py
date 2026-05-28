from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ThreatEvent
from app.db.repositories.threat_event_repository import ThreatEventRepository
from app.schemas.analytics_schema import DashboardMetrics
from app.schemas.threat_schema import ThreatEventRead


class AnalyticsService:
    """Read model service for dashboard analytics."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = ThreatEventRepository(session)

    async def latest_events(self, limit: int = 50) -> list[ThreatEventRead]:
        return [ThreatEventRead.model_validate(event) for event in await self.repo.latest(limit)]

    async def metrics(self) -> DashboardMetrics:
        result = await self.session.execute(
            select(func.count(ThreatEvent.id), func.avg(ThreatEvent.risk_score))
        )
        total, average = result.one()
        events = await self.repo.latest(1000)
        return DashboardMetrics(
            total_events=len(events) if total is None else int(total),
            blocked_events=sum(1 for event in events if event.decision == "block"),
            warned_events=sum(1 for event in events if event.decision == "warn"),
            allowed_events=sum(1 for event in events if event.decision == "allow"),
            average_risk=float(average or 0.0),
            categories=await self.repo.counts_by_category(),
        )
