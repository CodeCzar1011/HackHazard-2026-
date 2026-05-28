from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException, status

from app.core.security import (
    authenticate_dashboard_user,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.schemas.request_schema import LoginRequest, RefreshTokenRequest
from app.schemas.response_schema import AuthUser, TokenPairResponse


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenPairResponse)
async def login(payload: LoginRequest) -> TokenPairResponse:
    user = authenticate_dashboard_user(payload.email, payload.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenPairResponse(
        access_token=create_access_token(user),
        refresh_token=create_refresh_token(user),
        expires_in=30 * 60,
        user=user,
    )


@router.post("/refresh", response_model=TokenPairResponse)
async def refresh(payload: RefreshTokenRequest) -> TokenPairResponse:
    claims = decode_token(payload.refresh_token, expected_type="refresh")
    user = AuthUser(
        id=claims.get("sub", "admin-1"),
        name=claims.get("name", "GuardAIian Admin"),
        email=claims.get("email", "admin@guardaiian.local"),
        role=claims.get("role", "admin"),
    )
    return TokenPairResponse(
        access_token=create_access_token(user),
        refresh_token=create_refresh_token(user),
        expires_in=30 * 60,
        user=user,
    )


@router.get("/me", response_model=AuthUser)
async def me(authorization: str | None = Header(default=None, alias="Authorization")) -> AuthUser:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    claims = decode_token(authorization[len("Bearer ") :].strip(), expected_type="access")
    return AuthUser(
        id=claims.get("sub", "admin-1"),
        name=claims.get("name", "GuardAIian Admin"),
        email=claims.get("email", "admin@guardaiian.local"),
        role=claims.get("role", "admin"),
    )
