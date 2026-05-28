from __future__ import annotations

from app.utils.text_cleaner import normalize_text


def preprocess_prompt(prompt: str) -> str:
    return normalize_text(prompt)

