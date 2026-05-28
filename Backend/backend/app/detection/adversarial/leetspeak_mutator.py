from __future__ import annotations

TRANSLATION = str.maketrans({"a": "4", "e": "3", "i": "1", "o": "0", "s": "5", "t": "7"})


def leetspeak(text: str) -> str:
    return text.translate(TRANSLATION)

