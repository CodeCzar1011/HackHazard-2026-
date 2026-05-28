from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class WebSocketEvent(BaseModel):
    type: Literal["threat.blocked", "threat.warned", "threat.allowed", "dashboard.update"]
    payload: dict[str, Any] = Field(default_factory=dict)

