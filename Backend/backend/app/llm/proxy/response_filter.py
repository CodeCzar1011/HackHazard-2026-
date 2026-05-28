from __future__ import annotations

import re

SECRET_PATTERN = re.compile(r"(sk-[A-Za-z0-9]{12,}|api[_-]?key\s*[:=]\s*\S+|password\s*[:=]\s*\S+)", re.I)


def filter_response(text: str) -> tuple[str, list[str]]:
    """Redact obvious secrets from provider responses."""

    findings: list[str] = []
    if SECRET_PATTERN.search(text):
        findings.append("secret-like output redacted")
    return SECRET_PATTERN.sub("[REDACTED]", text), findings

