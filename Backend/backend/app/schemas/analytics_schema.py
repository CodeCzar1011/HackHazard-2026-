from __future__ import annotations

from pydantic import BaseModel


class DashboardMetrics(BaseModel):
    total_events: int
    blocked_events: int
    warned_events: int
    allowed_events: int
    average_risk: float
    categories: dict[str, int]

