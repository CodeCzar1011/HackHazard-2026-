from __future__ import annotations

import re

PATTERNS = [
    re.compile(r"\b(jailbreak|dan mode|unrestricted|no rules|bypass safety)\b", re.I),
    re.compile(r"\bact as\b.+\b(no policy|without restrictions|anything now)\b", re.I),
]


def score_jailbreak(text: str) -> tuple[float, list[str]]:
    hits = [pattern.pattern for pattern in PATTERNS if pattern.search(text)]
    return (min(1.0, 0.4 * len(hits)), ["jailbreak intent"] if hits else [])

