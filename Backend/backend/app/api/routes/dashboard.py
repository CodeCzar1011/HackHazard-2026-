from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.security import require_dashboard_api_key
from app.dependencies import DatabaseSession
from app.services.analytics_service import AnalyticsService


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", dependencies=[Depends(require_dashboard_api_key)])
async def dashboard_summary(session: DatabaseSession):
    service = AnalyticsService(session)
    return {"metrics": (await service.metrics()).model_dump(), "latest": [event.model_dump() for event in await service.latest_events(10)]}

