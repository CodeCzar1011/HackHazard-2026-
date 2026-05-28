from __future__ import annotations


class GuardAIianError(Exception):
    """Base application error for domain-specific failures."""


class PolicyBlockedError(GuardAIianError):
    """Raised when a request is blocked by the firewall."""


class ProviderUnavailableError(GuardAIianError):
    """Raised when a configured LLM provider cannot serve a request."""

