from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=20000)
    session_id: str = Field(default="default", max_length=128)
    provider: Literal["local", "openai", "anthropic", "gemini"] = "local"


class ChatRequest(AnalyzeRequest):
    forward_if_safe: bool = True


class LoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    password: str = Field(min_length=1, max_length=256)


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(min_length=8)

