from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


Decision = Literal["allow", "warn", "block"]


class DetectionSignal(BaseModel):
    name: str
    score: float = Field(ge=0, le=1)
    detail: str


class AnalyzeResponse(BaseModel):
    decision: Decision
    risk_score: float = Field(ge=0, le=1)
    category: str
    reasons: list[str]
    signals: list[DetectionSignal]
    session_id: str
    request_id: str


class ChatResponse(BaseModel):
    analysis: AnalyzeResponse
    provider: str
    output: str | None = None
    blocked: bool
    metadata: dict[str, Any] = Field(default_factory=dict)


class AuthUser(BaseModel):
    id: str
    name: str
    email: str
    role: Literal["admin", "analyst", "viewer"] = "admin"


class TokenPairResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: AuthUser

