from __future__ import annotations

LOOKALIKES = {"a": "а", "e": "е", "o": "о", "p": "р", "c": "с"}


def unicode_obfuscate(text: str) -> str:
    return "".join(LOOKALIKES.get(char, char) for char in text)

