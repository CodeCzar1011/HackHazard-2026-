from __future__ import annotations

from datetime import datetime, timedelta, timezone
import secrets

import jwt
from fastapi import Header, HTTPException, status
from jwt import InvalidTokenError

from app.core.config import settings
from app.schemas.response_schema import AuthUser


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _encode_token(*, subject: str, token_type: str, expires_delta: timedelta, claims: dict[str, str] | None = None) -> str:
    payload = {
        "sub": subject,
        "typ": token_type,
        "iat": int(_utc_now().timestamp()),
        "exp": int((_utc_now() + expires_delta).timestamp()),
    }
    if claims:
        payload.update(claims)
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_access_token(user: AuthUser) -> str:
    return _encode_token(
        subject=user.id,
        token_type="access",
        expires_delta=timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRES_MINUTES),
        claims={"email": user.email, "role": user.role, "name": user.name},
    )


def create_refresh_token(user: AuthUser) -> str:
    return _encode_token(
        subject=user.id,
        token_type="refresh",
        expires_delta=timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRES_DAYS),
        claims={"email": user.email, "role": user.role},
    )


def decode_token(token: str, expected_type: str = "access") -> dict[str, str]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
    if payload.get("typ") != expected_type:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
    return payload


def authenticate_dashboard_user(email: str, password: str) -> AuthUser | None:
    email_ok = secrets.compare_digest(email.strip().lower(), settings.DASHBOARD_ADMIN_EMAIL.strip().lower())
    password_ok = secrets.compare_digest(password, settings.DASHBOARD_ADMIN_PASSWORD)
    if not (email_ok and password_ok):
        return None
    return AuthUser(
        id="admin-1",
        name=settings.DASHBOARD_ADMIN_NAME,
        email=settings.DASHBOARD_ADMIN_EMAIL,
        role="admin",
    )


def _extract_bearer(authorization: str | None) -> str | None:
    if not authorization:
        return None
    prefix = "bearer "
    if authorization.lower().startswith(prefix):
        return authorization[len(prefix) :].strip()
    return None


async def require_dashboard_api_key(
    api_key: str | None = Header(default=None, alias=settings.API_KEY_HEADER_NAME),
    authorization: str | None = Header(default=None, alias="Authorization"),
) -> None:
    """Validate API key when dashboard/API-key auth is enabled."""

    if not settings.auth_required:
        return

    bearer = _extract_bearer(authorization)
    if bearer:
        decode_token(bearer, expected_type="access")
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
