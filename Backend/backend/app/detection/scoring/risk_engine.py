from __future__ import annotations

from dataclasses import dataclass

from app.core.config import settings


@dataclass(frozen=True)
class RiskInputs:
    semantic_similarity: float
    contextual_risk: float
    mutation_probability: float
    policy_score: float
    session_history: float


class RiskEngine:
    """Weighted adaptive risk scorer for firewall decisions."""

    def score(self, inputs: RiskInputs) -> float:
        weighted = (
            inputs.semantic_similarity * settings.SEMANTIC_RISK_WEIGHT
            + inputs.contextual_risk * settings.CONTEXT_RISK_WEIGHT
            + inputs.mutation_probability * settings.MUTATION_RISK_WEIGHT
            + inputs.policy_score * settings.REGEX_POLICY_WEIGHT
            + inputs.session_history * settings.SESSION_HISTORY_WEIGHT
        )
        return max(0.0, min(1.0, weighted))

