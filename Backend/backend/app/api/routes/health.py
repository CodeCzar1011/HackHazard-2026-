from __future__ import annotations

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse
from sqlalchemy import text

from app.core.config import settings
from app.db.session import get_engine
from app.vectorstore.chroma.chroma_client import get_chroma_client


router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
async def readiness():
    checks: dict[str, str] = {}
    ready = True

    try:
        async with get_engine().connect() as conn:
            await conn.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception:
        checks["database"] = "failed"
        ready = False

    try:
        get_chroma_client().heartbeat()
        checks["vectorstore"] = "ok"
    except Exception:
        checks["vectorstore"] = "failed"
        ready = False

    if settings.REDIS_URL:
        try:
            from redis.asyncio import from_url

            redis = from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
            await redis.ping()
            await redis.aclose()
            checks["redis"] = "ok"
        except Exception:
            checks["redis"] = "failed"
            ready = False
    else:
        checks["redis"] = "not_configured" if not settings.is_production else "failed"
        ready = ready and not settings.is_production

    body = {"status": "ready" if ready else "not_ready", "checks": checks}
    if ready:
        return body
    return ORJSONResponse(body, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

