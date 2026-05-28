from __future__ import annotations

import secrets

from fastapi import Header, HTTPException, status

from app.core.config import settings


async def require_dashboard_api_key(
    api_key: str | None = Header(default=None, alias=settings.API_KEY_HEADER_NAME),
) -> None:
    """Validate API key when dashboard/API-key auth is enabled."""

    if not settings.auth_required:
        return
    if not settings.DASHBOARD_API_KEY:
        if not settings.is_production and api_key:
            return
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key auth is not configured.",
        )
    if not api_key or not secrets.compare_digest(api_key, settings.DASHBOARD_API_KEY):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
