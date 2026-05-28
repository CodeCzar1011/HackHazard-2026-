from __future__ import annotations

from app.detection.classifiers.data_exfiltration import score_data_exfiltration
from app.detection.classifiers.jailbreak_detector import score_jailbreak
from app.detection.classifiers.prompt_injection import score_prompt_injection
from app.detection.classifiers.roleplay_attack import score_roleplay_attack


def score_policy_violations(text: str) -> tuple[float, list[str], str]:
    scorers = {
        "prompt_injection": score_prompt_injection,
        "jailbreak": score_jailbreak,
        "data_exfiltration": score_data_exfiltration,
        "roleplay_manipulation": score_roleplay_attack,
    }
    best_category = "benign"
    reasons: list[str] = []
    best_score = 0.0
    for category, scorer in scorers.items():
        score, category_reasons = scorer(text)
        reasons.extend(category_reasons)
        if score > best_score:
            best_score = score
            best_category = category
    return best_score, sorted(set(reasons)), best_category

