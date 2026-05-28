from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.security import require_dashboard_api_key
from app.dependencies import DatabaseSession
from app.schemas.analytics_schema import DashboardMetrics
from app.services.analytics_service import AnalyticsService


router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/metrics", response_model=DashboardMetrics, dependencies=[Depends(require_dashboard_api_key)])
async def metrics(session: DatabaseSession) -> DashboardMetrics:
    return await AnalyticsService(session).metrics()

