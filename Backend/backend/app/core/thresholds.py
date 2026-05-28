from __future__ import annotations

from dataclasses import dataclass

from app.core.config import settings


@dataclass(frozen=True)
class RiskThresholds:
    warn: float = settings.GLOBAL_WARN_THRESHOLD
    block: float = settings.GLOBAL_BLOCK_THRESHOLD


thresholds = RiskThresholds()

