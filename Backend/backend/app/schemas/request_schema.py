from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=20000)
    session_id: str = Field(default="default", max_length=128)
    provider: Literal["local", "openai", "anthropic", "gemini"] = "local"


class ChatRequest(AnalyzeRequest):
    forward_if_safe: bool = True

