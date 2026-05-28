from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ThreatEvent


class ThreatEventRepository:
    """Database access layer for threat/audit events."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, event: ThreatEvent) -> ThreatEvent:
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def latest(self, limit: int = 50) -> list[ThreatEvent]:
        result = await self.session.execute(
            select(ThreatEvent).order_by(ThreatEvent.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())

    async def counts_by_category(self) -> dict[str, int]:
        result = await self.session.execute(
            select(ThreatEvent.category, func.count(ThreatEvent.id)).group_by(ThreatEvent.category)
        )
        return {str(category): int(count) for category, count in result.all()}

