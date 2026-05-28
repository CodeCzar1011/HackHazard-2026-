from __future__ import annotations

from app.core.config import settings
from app.schemas.response_schema import Decision


def decide(risk_score: float) -> Decision:
    if risk_score >= settings.GLOBAL_BLOCK_THRESHOLD:
        return "block"
    if risk_score >= settings.GLOBAL_WARN_THRESHOLD:
        return "warn"
    return "allow"

