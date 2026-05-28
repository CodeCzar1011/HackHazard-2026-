from __future__ import annotations

from app.detection.contextual.session_memory import SessionTurn
from app.utils.text_cleaner import lowercase_for_matching


ESCALATION_TERMS = ("later", "next", "step by step", "continue", "remember", "from now on")


def score_contextual_risk(prompt: str, history: list[SessionTurn]) -> tuple[float, list[str]]:
    """Score multi-turn escalation and session poisoning indicators."""

    if not history:
        return 0.0, []
    reasons: list[str] = []
    recent_high_risk = sum(1 for turn in history[-5:] if turn.risk_score >= 0.55)
    score = min(0.45, recent_high_risk * 0.12)
    lowered = lowercase_for_matching(prompt)
    if any(term in lowered for term in ESCALATION_TERMS) and recent_high_risk:
        score += 0.25
        reasons.append("multi-turn escalation after risky prompts")
    if any(turn.category in {"jailbreak", "prompt_injection"} for turn in history[-3:]):
        score += 0.1
        reasons.append("recent jailbreak or injection context")
    return min(1.0, score), reasons

