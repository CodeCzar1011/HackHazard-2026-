from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Float, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ThreatEvent(Base):
    """Persisted security decision for audit, dashboards, and analytics."""

    __tablename__ = "threat_events"

    session_id: Mapped[str] = mapped_column(String(128), index=True)
    provider: Mapped[str] = mapped_column(String(32), default="local")
    prompt: Mapped[str] = mapped_column(Text)
    decision: Mapped[str] = mapped_column(String(16), index=True)
    risk_score: Mapped[float] = mapped_column(Float, index=True)
    category: Mapped[str] = mapped_column(String(64), index=True)
    reasons: Mapped[list[str]] = mapped_column(JSON, default=list)
    signals: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

