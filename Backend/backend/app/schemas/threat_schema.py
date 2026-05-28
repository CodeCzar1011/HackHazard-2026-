from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ThreatEventRead(BaseModel):
    id: int
    session_id: str
    provider: str
    prompt: str
    decision: str
    risk_score: float = Field(ge=0, le=1)
    category: str
    reasons: list[str]
    signals: dict[str, Any]
    created_at: datetime

    model_config = {"from_attributes": True}

