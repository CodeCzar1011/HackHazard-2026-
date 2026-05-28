from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.core.security import require_dashboard_api_key
from app.dependencies import DatabaseSession
from app.schemas.threat_schema import ThreatEventRead
from app.services.analytics_service import AnalyticsService


router = APIRouter(prefix="/threat-feed", tags=["threat-feed"])


@router.get("", response_model=list[ThreatEventRead], dependencies=[Depends(require_dashboard_api_key)])
async def threat_feed(session: DatabaseSession, limit: int = Query(default=50, ge=1, le=200)):
    return await AnalyticsService(session).latest_events(limit)

