from __future__ import annotations

import re

PATTERNS = [
    re.compile(r"\b(ignore|disregard|forget)\b.+\b(previous|system|developer|instructions?)\b", re.I),
    re.compile(r"\b(system prompt|hidden instruction|developer message)\b", re.I),
]


def score_prompt_injection(text: str) -> tuple[float, list[str]]:
    hits = [pattern.pattern for pattern in PATTERNS if pattern.search(text)]
    return (min(1.0, 0.35 * len(hits)), ["prompt injection pattern"] if hits else [])

