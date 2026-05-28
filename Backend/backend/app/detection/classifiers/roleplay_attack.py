from __future__ import annotations

import re

PATTERNS = [
    re.compile(r"\b(roleplay|pretend|simulate|act as)\b.+\b(unrestricted|evil|developer|admin)\b", re.I),
    re.compile(r"\bfrom now on\b.+\b(no safety|no rules|ignore policy)\b", re.I),
]


def score_roleplay_attack(text: str) -> tuple[float, list[str]]:
    hits = [pattern.pattern for pattern in PATTERNS if pattern.search(text)]
    return (min(1.0, 0.35 * len(hits)), ["roleplay manipulation"] if hits else [])

