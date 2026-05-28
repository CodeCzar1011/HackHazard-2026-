from __future__ import annotations

from fastapi import APIRouter

from app.api.routes.admin import router as admin_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes.analyze import router as analyze_router
from app.api.routes.auth import router as auth_router
from app.api.routes.chat import router as chat_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.health import router as health_router
from app.api.routes.threat_feed import router as threat_feed_router
from app.api.routes.readiness import router as readiness_router
from app.api.routes.websocket import router as websocket_router


api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(readiness_router, tags=["health"])
api_router.include_router(auth_router)
api_router.include_router(analyze_router)
api_router.include_router(chat_router)
api_router.include_router(analytics_router)
api_router.include_router(dashboard_router)
api_router.include_router(threat_feed_router)
api_router.include_router(admin_router)
api_router.include_router(websocket_router)

