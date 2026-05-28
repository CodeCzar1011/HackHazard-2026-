from __future__ import annotations

import re

PATTERNS = [
    re.compile(r"\b(api[_ -]?key|secret|token|password|credential|private key|env variables?)\b", re.I),
    re.compile(r"\b(print|show|dump|reveal|exfiltrate)\b.+\b(secrets?|keys?|tokens?|credentials?)\b", re.I),
]


def score_data_exfiltration(text: str) -> tuple[float, list[str]]:
    hits = [pattern.pattern for pattern in PATTERNS if pattern.search(text)]
    return (min(1.0, 0.45 * len(hits)), ["data exfiltration intent"] if hits else [])

