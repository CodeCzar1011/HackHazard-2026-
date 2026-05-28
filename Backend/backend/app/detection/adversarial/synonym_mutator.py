from __future__ import annotations

SYNONYMS = {
    "ignore": "disregard",
    "reveal": "expose",
    "show": "display",
    "secret": "credential",
    "instructions": "directives",
}


def synonym_replace(text: str) -> str:
    words = text.split()
    return " ".join(SYNONYMS.get(word.lower(), word) for word in words)

