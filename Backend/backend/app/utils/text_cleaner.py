from __future__ import annotations

import re
import unicodedata


WHITESPACE_RE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    """Normalize user input while preserving useful attack indicators."""

    normalized = unicodedata.normalize("NFKC", text)
    return WHITESPACE_RE.sub(" ", normalized).strip()


def lowercase_for_matching(text: str) -> str:
    return normalize_text(text).casefold()

