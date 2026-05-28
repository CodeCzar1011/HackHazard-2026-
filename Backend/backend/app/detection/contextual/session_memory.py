from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field

from app.core.config import settings


@dataclass
class SessionTurn:
    prompt: str
    risk_score: float
    decision: str
    category: str


@dataclass
class SessionState:
    turns: deque[SessionTurn] = field(
        default_factory=lambda: deque(maxlen=settings.HIGH_RISK_CONTEXT_WINDOW)
    )


class SessionMemory:
    """In-process session memory for contextual risk during demo/runtime."""

    def __init__(self) -> None:
        self._sessions: dict[str, SessionState] = defaultdict(SessionState)

    def get_history(self, session_id: str) -> list[SessionTurn]:
        return list(self._sessions[session_id].turns)

    def add_turn(self, session_id: str, turn: SessionTurn) -> None:
        self._sessions[session_id].turns.append(turn)


session_memory = SessionMemory()

